export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";

async function postJSON<TReq, TRes>(path: string, body: TReq): Promise<TRes> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let msg = `HTTP ${res.status}`;
    try {
      const data = await res.json();
      msg = data?.detail ? String(data.detail) : JSON.stringify(data);
    } catch {}
    throw new Error(msg);
  }

  return (await res.json()) as TRes;
}

export type GreeksReq = {
  S0: number;
  K: number;
  r: number;
  sigma: number;
  T: number;
  option_type: "call" | "put";
};

export type GreeksRes = {
  price: number;
  greeks: {
    delta: number;
    gamma: number;
    theta: number;
    vega: number;
    rho: number;
  };
  inputs: GreeksReq;
};

export type HedgeReq = {
  S0: number;
  K: number;
  r: number;
  T: number;
  option_type: "call" | "put";
  true_sigma: number;
  assumed_sigma: number;
  n_paths: number;
  n_steps: number;
  transaction_cost_bps: number;
  seed: number;
  short_option: boolean;
};


export type HedgeRes = {
  option_price0: number;
  summary: {
    mean_pnl: number;
    std_pnl: number;
    var_95: number;
    cvar_95: number;
    prob_loss: number;
  };
  histogram: {
    bin_edges: number[];
    counts: number[];
  };
  sample_path: {
    t: number[];
    S: number[];
    delta: number[];
    shares: number[];
    cash: number[];
  };
};

export const api = {
  greeks: (req: GreeksReq) => postJSON<GreeksReq, GreeksRes>("/api/greeks", req),
  hedgeSim: (req: HedgeReq) =>
    postJSON<HedgeReq, HedgeRes>("/api/hedge/simulate", req),
};
