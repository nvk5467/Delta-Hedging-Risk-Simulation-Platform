from enum import Enum
from pydantic import BaseModel, Field

class OptionType(str, Enum):
    CALL = "call"
    PUT = "put"

class GreeksRequest(BaseModel):
    S0: float = Field(..., gt=0, description="Initial stock price")
    K: float = Field(..., gt=0, description="Strike price")
    r: float = Field(..., description="Risk-free rate (decimal, e.g. 0.05)")
    sigma: float = Field(..., gt=0, description="Volatility (decimal, e.g. 0.2)")
    T: float = Field(..., gt=0, description="Time to maturity in years")
    option_type: OptionType = Field(..., description="call or put")

class Greeks(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


class GreeksResponse(BaseModel):
    price: float
    greeks: Greeks
    inputs: GreeksRequest