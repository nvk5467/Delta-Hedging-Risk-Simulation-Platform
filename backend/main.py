from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.greeks import router as greeks_router
from api.routers.health import router as health_router
from api.routers.hedge import router as hedge_router

app = FastAPI(title="Hedging Lab API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # for Next.js later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hedge_router)
app.include_router(health_router)
app.include_router(greeks_router, prefix = "/api")