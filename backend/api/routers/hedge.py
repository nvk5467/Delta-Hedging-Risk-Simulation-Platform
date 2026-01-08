from __future__ import annotations
from fastapi import APIRouter, HTTPException
from api.schemas.hedge import (
    HedgeSimRequest, HedgeSimResponse, SummaryStats, Histogram, SamplePathSeries,
    ConvergenceRequest, ConvergenceResponse, ConvergencePoint
)

from api.core.paths import simulate_gbm_paths
from api.core.hedging import hedge_monte_carlo
from api.core.stats import compute_summary_stats, compute_histogram

router = APIRouter(prefix="/api/hedge", tags=["hedge"])

@router.post("/simulate", response_model=HedgeSimResponse)
def simulate(req: HedgeSimRequest) -> HedgeSimResponse:
    try:
        # 1) simulate stock paths with TRUE volatility
        paths = simulate_gbm_paths(
            S0=req.S0,
            r=req.r,
            sigma=req.true_sigma,
            T=req.T,
            n_steps=req.n_steps,
            n_paths=req.n_paths,
            seed=req.seed,
        )

        # 2) hedge across paths using ASSUMED volatility (for delta)
        mc = hedge_monte_carlo(
            paths=paths,
            K=req.K,
            r=req.r,
            assumed_sigma=req.assumed_sigma,
            T=req.T,
            option_type=req.option_type.value,
            transaction_cost_bps=req.transaction_cost_bps,
            short_option=req.short_option,
        )

        # 3) compute risk stats + histogram over PnLs
        stats = compute_summary_stats(mc.pnls)
        hist = compute_histogram(mc.pnls, n_bins=40)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 4) convert numpy arrays -> lists for JSON
    sp = mc.sample_series

    return HedgeSimResponse(
        option_price0=float(mc.option_price0),
        summary=SummaryStats(
            mean_pnl=float(stats.mean_pnl),
            std_pnl=float(stats.std_pnl),
            var_95=float(stats.var_95),
            cvar_95=float(stats.cvar_95),
            prob_loss=float(stats.prob_loss),
        ),
        histogram=Histogram(
            bin_edges=[float(x) for x in hist.bin_edges],
            counts=[int(c) for c in hist.counts],
        ),
        sample_path=SamplePathSeries(
            t=[float(x) for x in sp.t],
            S=[float(x) for x in sp.S],
            delta=[float(x) for x in sp.delta],
            shares=[float(x) for x in sp.shares],
            cash=[float(x) for x in sp.cash],
        ),
    )

@router.post("/convergence", response_model=ConvergenceResponse)
def convergence(req: ConvergenceRequest) -> ConvergenceResponse:
    try:
        if any(s <= 0 for s in req.steps_list):
            raise ValueError("All n_steps in steps_list must be > 0")
        if len(req.steps_list) == 0:
            raise ValueError("steps_list must be non-empty")

        # Use the same option premium for all points (based on assumed sigma)
        from api.core.bs import bs_price_and_greeks  # local import avoids circulars
        option_price0 = bs_price_and_greeks(
            S0=req.S0,
            K=req.K,
            r=req.r,
            sigma=req.assumed_sigma,
            T=req.T,
            option_type=req.option_type.value,
        ).price

        points: list[ConvergencePoint] = []

        # Run each step setting
        for n_steps in req.steps_list:
            paths = simulate_gbm_paths(
                S=req.S0,
                r=req.r,
                sigma=req.true_sigma,
                T=req.T,
                n_steps=n_steps,
                n_paths=req.n_paths,
                seed=req.seed,
            )

            mc = hedge_monte_carlo(
                paths=paths,
                K=req.K,
                r=req.r,
                assumed_sigma=req.assumed_sigma,
                T=req.T,
                option_type=req.option_type.value,
                transaction_cost_bps=req.transaction_cost_bps,
                short_option=req.short_option,
            )

            stats = compute_summary_stats(mc.pnls)

            points.append(
                ConvergencePoint(
                    n_steps=int(n_steps),
                    mean_pnl=float(stats.mean_pnl),
                    std_pnl=float(stats.std_pnl),
                    var_95=float(stats.var_95),
                    cvar_95=float(stats.cvar_95),
                    prob_loss=float(stats.prob_loss),
                )
            )

        # Sort so frontend charts are clean
        points.sort(key=lambda p: p.n_steps)

        return ConvergenceResponse(option_price0=float(option_price0), points=points)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
