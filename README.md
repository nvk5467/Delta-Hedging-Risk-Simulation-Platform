# Delta Hedging & Risk Simulation Platform

An interactive web application for computing **Black–Scholes option Greeks** and running **Monte Carlo delta-hedging simulations** to evaluate hedging performance and risk. Built with a **FastAPI backend** and **Next.js frontend**.

This project emphasizes **API-driven numerical computation**, transforming large stochastic simulations into concise, actionable risk metrics suitable for real-world API consumers.

---

## Features

### Backend (FastAPI)
- **Black–Scholes Pricing & Greeks**
  - Price, Delta, Gamma, Theta, Vega, Rho
  - European call and put options
- **Monte Carlo Simulation**
  - Geometric Brownian Motion (GBM) price paths
  - Configurable number of paths and rebalancing steps
- **Delta Hedging Engine**
  - Dynamic portfolio rebalancing using option delta
  - Support for long or short option positions
  - Optional transaction costs
- **Risk Aggregation**
  - Mean and standard deviation of PnL
  - Value at Risk (VaR) and Conditional VaR (CVaR)
  - Probability of loss
  - PnL histogram data (bins + counts)
- **Typed API Contracts**
  - Validated Pydantic request/response schemas
  - Auto-generated Swagger documentation

### Frontend (Next.js)
- Parameterized Greeks calculator UI
- Delta-hedging simulator UI
- Visualization-ready API responses
- Clear separation of computation (backend) and presentation (frontend)

---

## Project Structure

```
Finance App/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── routers/             # API route handlers
│   │   ├── schemas/             # Pydantic request/response models
│   │   └── core/                # Quant logic (BS, paths, hedging)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   └── lib/                 # Typed API client
│   └── package.json
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

---

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

Backend available at:
- API: http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend available at:
```
http://localhost:3000
```

---

## Running the Application

**Terminal 1 (backend):**
```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

**Terminal 2 (frontend):**
```bash
cd frontend
npm run dev
```

---

## API Endpoints

### POST `/api/greeks`
Compute Black–Scholes price and Greeks.

```json
{
  "S0": 100,
  "K": 100,
  "r": 0.05,
  "sigma": 0.2,
  "T": 1.0,
  "option_type": "call"
}
```

---

### POST `/api/hedge/simulate`
Run Monte Carlo GBM paths and delta hedging.

```json
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
```

---
