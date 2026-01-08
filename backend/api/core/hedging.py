from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Literal
import numpy as np
from api.core.bs import bs_price_and_greeks
from typing import Literal

OptionType = Literal["call", "put"]

@dataclass(frozen=True)
class HedgePathSeries:
    t: np.ndarray          
    S: np.ndarray          
    delta: np.ndarray      
    shares: np.ndarray     
    cash: np.ndarray      

@dataclass(frozen=True)
class HedgeOnePathResult:
    pnl: float
    series: HedgePathSeries

@dataclass(frozen=True)
class HedgeMCResult:
    pnls: np.ndarray              
    sample_series: HedgePathSeries 
    option_price0: float   

def _transaction_cost(cost_notional: float, bps: float) -> float:
    if bps <= 0:
        return 0.0
    return abs(cost_notional) * (bps / 10000.0)

def option_payoff(ST: float, K: float, option_type: OptionType) -> float:
    if option_type == "call":
        return max(ST - K, 0.0)
    return max(K - ST, 0.0)

def hedge_one_path(
    S_path: np.ndarray,
    K: float,
    r: float,
    assumed_sigma: float,
    T: float,
    option_type: OptionType,
    transaction_cost_bps: float = 0.0,
    short_option: bool = True,
) -> HedgeOnePathResult:
    if K <= 0 or T <= 0 or assumed_sigma <= 0:
        raise ValueError("K, T, assumed_sigma must be > 0")
    if S_path.ndim != 1 or len(S_path) < 2:
        raise ValueError("S_path must be 1D array of length >= 2")

    n_steps = len(S_path) - 1
    dt = T / n_steps

    # Pre-allocate arrays
    t_arr = np.linspace(0.0, T, n_steps + 1)
    delta_arr = np.empty(n_steps + 1, dtype=float)
    shares_arr = np.empty(n_steps + 1, dtype=float)
    cash_arr = np.empty(n_steps + 1, dtype=float)

    # --- time 0: price option + set initial hedge ---
    S0 = float(S_path[0])
    g0 = bs_price_and_greeks(S=S0, K=K, r=r, sigma=assumed_sigma, T=T, option_type=option_type)
    option_price0 = g0.price
    delta0 = g0.delta

    # If we short the option, we receive premium; if long, we pay premium.
    cash = option_price0 if short_option else -option_price0
    shares = 0.0

    # Buy/sell shares to reach target delta
    trade_shares = delta0 - shares
    notional = trade_shares * S0
    tc = _transaction_cost(notional, transaction_cost_bps)

    cash -= notional
    cash -= tc
    shares = delta0

    delta_arr[0] = delta0
    shares_arr[0] = shares
    cash_arr[0] = cash

    # --- rebalance at each step ---
    for step in range(1, n_steps + 1):
        # accrue interest on cash over dt
        cash *= math.exp(r * dt)

        S = float(S_path[step])
        time_remaining = T - step * dt

        if time_remaining > 0:
            g = bs_price_and_greeks(
                S=S,
                K=K,
                r=r,
                sigma=assumed_sigma,
                T=time_remaining,
                option_type=option_type,
            )
            target_delta = g.delta
        else:
            # at maturity, delta isn't needed for rebalancing (we stop)
            target_delta = delta_arr[step - 1]

        # rebalance except at maturity (optional; here we still record values)
        if time_remaining > 0:
            trade_shares = target_delta - shares
            notional = trade_shares * S
            tc = _transaction_cost(notional, transaction_cost_bps)

            cash -= notional
            cash -= tc
            shares = target_delta

        delta_arr[step] = target_delta
        shares_arr[step] = shares
        cash_arr[step] = cash

    # --- maturity: compute PnL ---
    ST = float(S_path[-1])
    payoff = option_payoff(ST, K, option_type)

    portfolio_value = shares * ST + cash
    pnl = portfolio_value - payoff

    series = HedgePathSeries(
        t=t_arr,
        S=S_path.astype(float),
        delta=delta_arr,
        shares=shares_arr,
        cash=cash_arr,
    )
    return HedgeOnePathResult(pnl=pnl, series=series)

def hedge_monte_carlo(
    paths: np.ndarray,
    K: float,
    r: float,
    assumed_sigma: float,
    T: float,
    option_type: OptionType,
    transaction_cost_bps: float = 0.0,
    short_option: bool = True,
) -> HedgeMCResult:
    if paths.ndim != 2 or paths.shape[1] < 2:
        raise ValueError("paths must be 2D array (n_paths, n_steps+1) with n_steps+1 >= 2")

    n_paths = paths.shape[0]
    pnls = np.empty(n_paths, dtype=float)

    sample_series = None
    option_price0 = None

    for i in range(n_paths):
        res = hedge_one_path(
            S_path=paths[i],
            K=K,
            r=r,
            assumed_sigma=assumed_sigma,
            T=T,
            option_type=option_type,
            transaction_cost_bps=transaction_cost_bps,
            short_option=short_option,
        )
        pnls[i] = res.pnl
        if i == 0:
            sample_series = res.series
            # compute option premium again (or extract it by recomputing)
            S0 = float(paths[i, 0])
            option_price0 = bs_price_and_greeks(
                S=S0, K=K, r=r, sigma=assumed_sigma, T=T, option_type=option_type
            ).price

    assert sample_series is not None
    assert option_price0 is not None

    return HedgeMCResult(pnls=pnls, sample_series=sample_series, option_price0=float(option_price0))