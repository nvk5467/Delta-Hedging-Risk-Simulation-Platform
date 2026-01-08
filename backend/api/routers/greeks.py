from fastapi import APIRouter, HTTPException

from api.schemas.greeks import GreeksRequest, GreeksResponse, Greeks
from api.core.bs import bs_price_and_greeks

router = APIRouter(tags=["greeks"])


@router.post("/greeks", response_model=GreeksResponse)
def compute_greeks(req: GreeksRequest) -> GreeksResponse:
    try:
        result = bs_price_and_greeks(
            S=req.S0,
            K=req.K,
            r=req.r,
            sigma=req.sigma,
            T=req.T,
            option_type=req.option_type.value
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    greeks = Greeks(
        delta=result.delta,
        gamma=result.gamma,
        theta=result.theta,
        vega=result.vega,
        rho=result.rho
    )

    return GreeksResponse(
        price=result.price,
        greeks=greeks,
        inputs=req
    )