# Delta-Hedging-Risk-Simulation-PlatformDelta Hedging & Risk Simulation Platform

An interactive web application for computing Black–Scholes option Greeks and running Monte Carlo delta-hedging simulations to evaluate hedging performance and risk. Built with a FastAPI backend and Next.js frontend.

Features
API-Driven Quant Analytics

Greeks + Pricing (Black–Scholes): Compute price + Delta, Gamma, Theta, Vega, Rho for European calls/puts

Delta Hedging Simulation: Simulate a dynamically rebalanced hedged portfolio over GBM paths

Risk Summary Output: API returns actionable risk metrics instead of raw simulation dumps:

Mean / Std PnL

VaR / CVaR

Probability of loss

PnL histogram bins/counts

Sample Path Output: Returns one representative simulated path (time series) for visualization

Visualizations (Frontend)

Display Greeks output and formatted result cards

Plot-ready data returned from API:

PnL histogram

Sample GBM path + hedge shares/cash series

(Optional) replication error / PnL over time

Project Structure
Finance App/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app + router registration
│   │   ├── routers/             # Route handlers (greeks, hedge)
│   │   ├── schemas/             # Pydantic request/response models
│   │   └── core/                # Quant logic (bs, paths, hedging)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js app router pages
│   │   └── lib/                 # Typed API client + helpers
│   └── package.json
└── README.md

Setup Instructions
Prerequisites

Python 3.10+ recommended (3.12 works)

Node.js 18+ and npm

Backend Setup

From the project root:

cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000


Backend runs at:

API: http://127.0.0.1:8000

Swagger docs: http://127.0.0.1:8000/docs

Frontend Setup

From the project root:

cd frontend
npm install
npm run dev


Frontend runs at:

http://localhost:3000

Running the Application

Terminal 1 (backend):

cd backend
uvicorn api.main:app --reload --port 8000


Terminal 2 (frontend):

cd frontend
npm run dev


Open:

http://localhost:3000

Usage
Greeks Calculator

Enter parameters:

Initial Stock Price (S₀)

Strike (K)

Risk-Free Rate (r)

Volatility (σ)

Time to Maturity (T)

Option Type (Call/Put)

Click Calculate → backend returns price + Greeks.

Hedging Simulation

Enter simulation parameters:

True volatility vs assumed volatility

Number of paths

Steps per path (rebalancing frequency)

Transaction costs (bps)

Long/short option position

Click Simulate → backend returns PnL risk summary + histogram + sample path.

API Endpoints
POST /api/greeks

Compute Black–Scholes price + Greeks.

Request Body

{
  "S0": 100,
  "K": 100,
  "r": 0.05,
  "sigma": 0.2,
  "T": 1.0,
  "option_type": "call"
}


Response (example)

{
  "price": 10.450583572185565,
  "greeks": {
    "delta": 0.6368306511756191,
    "gamma": 0.018762017345846895,
    "theta": -6.414027546438197,
    "vega": 37.52403469169379,
    "rho": 53.232481545376345
  },
  "inputs": {
    "S0": 100,
    "K": 100,
    "r": 0.05,
    "sigma": 0.2,
    "T": 1,
    "option_type": "call"
  }
}

POST /api/hedge/simulate

Run Monte Carlo GBM paths + delta hedging and return risk metrics + histogram + sample path.

Request Body

{
  "S0": 100,
  "K": 100,
  "r": 0.05,
  "T": 1.0,
  "option_type": "call",
  "true_sigma": 0.2,
  "assumed_sigma": 0.2,
  "n_paths": 2000,
  "n_steps": 252,
  "transaction_cost_bps": 0,
  "seed": 1,
  "short_option": true
}


Response (high-level)

{
  "option_price0": 10.45058,
  "summary": {
    "mean_pnl": 0.0062,
    "std_pnl": 0.4349,
    "var_95": -0.7182,
    "cvar_95": -1.0026,
    "prob_loss": 0.4788
  },
  "histogram": { "bin_edges": [...], "counts": [...] },
  "sample_path": { "t": [...], "S": [...], "delta": [...], "shares": [...], "cash": [...] }
}