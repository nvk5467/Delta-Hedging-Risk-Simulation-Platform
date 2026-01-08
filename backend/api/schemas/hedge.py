from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field


class OptionType(str, Enum):
    call = "call"
    put = "put"


class HedgeSimRequest(BaseModel):
    S0: float = Field(..., gt=0)
    K: float = Field(..., gt=0)
    r: float = Field(...)
    T: float = Field(..., gt=0)
    option_type: OptionType = Field(...)

    true_sigma: float = Field(..., gt=0, description="Vol used to simulate paths")
    assumed_sigma: float = Field(..., gt=0, description="Vol used for delta/BS in hedge")

    n_paths: int = Field(2000, ge=1, le=50000)
    n_steps: int = Field(252, ge=1, le=5000)

    transaction_cost_bps: float = Field(0.0, ge=0.0, le=100.0)
    seed: int | None = Field(None)

    short_option: bool = Field(True, description="True = sell option then hedge; False = buy then hedge")

class SummaryStats(BaseModel):
    mean_pnl: float
    std_pnl: float
    var_95: float
    cvar_95: float
    prob_loss: float


class Histogram(BaseModel):
    bin_edges: list[float]
    counts: list[int]


class SamplePathSeries(BaseModel):
    t: list[float]
    S: list[float]
    delta: list[float]
    shares: list[float]
    cash: list[float]


class HedgeSimResponse(BaseModel):
    option_price0: float
    summary: SummaryStats
    histogram: Histogram
    sample_path: SamplePathSeries

class ConvergenceRequest(BaseModel):
    S0: float = Field(..., gt=0)
    K: float = Field(..., gt=0)
    r: float = Field(...)
    T: float = Field(..., gt=0)
    option_type: OptionType = Field(...)

    true_sigma: float = Field(..., gt=0)
    assumed_sigma: float = Field(..., gt=0)

    n_paths: int = Field(2000, ge=1, le=50000)
    steps_list: list[int] = Field(default_factory=lambda: [12, 52, 252, 1000])

    transaction_cost_bps: float = Field(0.0, ge=0.0, le=100.0)
    seed: int | None = Field(None)
    short_option: bool = Field(True)


class ConvergencePoint(BaseModel):
    n_steps: int
    mean_pnl: float
    std_pnl: float
    var_95: float
    cvar_95: float
    prob_loss: float


class ConvergenceResponse(BaseModel):
    option_price0: float
    points: list[ConvergencePoint]