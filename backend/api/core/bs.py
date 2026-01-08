from scipy.stats import norm
from dataclasses import dataclass
from typing import Literal
import math


@dataclass(frozen=True)
class BSResult:
    price: float
    delta: float
    gamma: float
    theta: float  # per year
    vega: float   # per 1.0 volatility (so per 1% is vega/100)
    rho: float    # per 1.0 rate (so per 1% is rho/100)

def bs_price_and_greeks(
    S: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    option_type: Literal["call", "put"]
) -> BSResult:
    if S <= 0 or K <= 0 or sigma <= 0 or T <= 0:
        raise ValueError("S, K, sigma, and T must be > 0.")
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'.")
    
    sqrt_T = math.sqrt(T)
    d1 = (math.log(S/K) + (r + .5 * sigma**2) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T

    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)
    n_d1 = norm.pdf(d1)
    disc = math.exp(-r * T)

    if option_type == "call":
        price = S * N_d1 - K * disc * N_d2
        delta = N_d1
        rho = K * T * disc * N_d2
        theta = -(S * n_d1 * sigma) / (2.0 * sqrt_T) - r * K * disc * N_d2
    else:
        N_minus_d1 = norm.cdf(-d1)
        N_minus_d2 = norm.cdf(-d2)
        price = K * disc * N_minus_d2 - S * N_minus_d1
        delta = N_d1 - 1.0
        rho = -K * T * disc * N_minus_d2
        theta = -(S * n_d1 * sigma) / (2.0 * sqrt_T) + r * K * disc * N_minus_d2

    gamma = n_d1 / (S * sigma * sqrt_T)
    vega = S * n_d1 * sqrt_T

    return BSResult(price=price, delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)