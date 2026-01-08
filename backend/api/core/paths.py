from __future__ import annotations

import numpy as np


def simulate_gbm_paths(
    S0: float,
    r: float,
    sigma: float,
    T: float,
    n_steps: int,
    n_paths: int,
    seed: int | None = None,
) -> np.ndarray:
    
    if S0 <= 0:
        raise ValueError("S0 must be > 0")
    if sigma <= 0:
        raise ValueError("sigma must be > 0")
    if T <= 0:
        raise ValueError("T must be > 0")
    if n_steps <= 0:
        raise ValueError("n_steps must be > 0")
    if n_paths <= 0:
        raise ValueError("n_paths must be > 0")

    dt = T / n_steps
    rng = np.random.default_rng(seed)

    # Z ~ N(0,1) for each path and time step
    Z = rng.standard_normal(size=(n_paths, n_steps))

    # Exact GBM step: S_{t+dt} = S_t * exp((r - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
    drift = (r - 0.5 * sigma * sigma) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    log_returns = drift + diffusion  # shape (n_paths, n_steps)

    # Build paths by cumulative product of exp(log_returns)
    paths = np.empty((n_paths, n_steps + 1), dtype=float)
    paths[:, 0] = S0
    paths[:, 1:] = S0 * np.exp(np.cumsum(log_returns, axis=1))

    return paths

def simulate_gbm_path(
    S0: float,
    r: float,
    sigma: float,
    T: float,
    n_steps: int,
    seed: int | None = None,
) -> np.ndarray:
    
    return simulate_gbm_paths(S0, r, sigma, T, n_steps, n_paths=1, seed=seed)[0]