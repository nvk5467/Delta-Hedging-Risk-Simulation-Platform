from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class SummaryStats:
    mean_pnl: float
    std_pnl: float
    var_95: float     
    cvar_95: float    
    prob_loss: float 

@dataclass(frozen=True)
class Histogram:
    bin_edges: list[float]
    counts: list[int]

def compute_summary_stats(pnls: np.ndarray) -> SummaryStats:
    if pnls.ndim != 1 or pnls.size == 0:
        raise ValueError("pnls must be a non-empty 1D array")

    mean = float(np.mean(pnls))
    std = float(np.std(pnls, ddof=1)) if pnls.size > 1 else 0.0
    prob_loss = float(np.mean(pnls < 0.0))

    # VaR_95 = 5th percentile of PnL (worst 5% outcomes)
    var_95 = float(np.quantile(pnls, 0.05))

    # CVaR_95 = average PnL conditional on being in worst 5%
    tail = pnls[pnls <= var_95]
    cvar_95 = float(np.mean(tail)) if tail.size > 0 else var_95

    return SummaryStats(
        mean_pnl=mean,
        std_pnl=std,
        var_95=var_95,
        cvar_95=cvar_95,
        prob_loss=prob_loss,
    )

def compute_histogram(pnls: np.ndarray, n_bins: int = 40) -> Histogram:
    if pnls.ndim != 1 or pnls.size == 0:
        raise ValueError("pnls must be a non-empty 1D array")
    if n_bins <= 1:
        raise ValueError("n_bins must be > 1")

    counts, edges = np.histogram(pnls, bins=n_bins)
    return Histogram(
        bin_edges=[float(x) for x in edges],
        counts=[int(c) for c in counts],
    )


