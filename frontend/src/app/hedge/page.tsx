"use client";

import { useState } from "react";
import { api, HedgeRes } from "@/lib/api";
import {
  PnLHistogramChart,
  SamplePathChart,
  HedgePositionChart,
} from "@/components/charts";

export default function HedgePage() {
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [res, setRes] = useState<HedgeRes | null>(null);

  async function run() {
    setLoading(true);
    setErr(null);
    try {
      const out = await api.hedgeSim({
        S0: 100,
        K: 100,
        r: 0.05,
        T: 1,
        option_type: "call",
        true_sigma: 0.2,
        assumed_sigma: 0.2,
        n_paths: 2000,
        n_steps: 252,
        transaction_cost_bps: 0,
        seed: 1,
        short_option: true,
    });

      setRes(out);
    } catch (e: any) {
      setErr(e?.message ?? "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-zinc-50 p-6">
      <div className="mx-auto max-w-3xl space-y-6">
        <h1 className="text-2xl font-bold">Delta Hedging Simulator</h1>

        <button
          onClick={run}
          disabled={loading}
          className="rounded-xl bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
        >
          {loading ? "Simulating..." : "Run simulation"}
        </button>

        {err && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-800">
            {err}
          </div>
        )}

        {res && (
        <section className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm space-y-6">
            <div className="text-sm">
            <span className="font-medium">Option price (t=0):</span>{" "}
            {res.option_price0.toFixed(6)}
            </div>

            <div className="grid grid-cols-2 gap-2 text-sm">
            <Stat k="Mean PnL" v={res.summary.mean_pnl} />
            <Stat k="Std PnL" v={res.summary.std_pnl} />
            <Stat k="VaR 95%" v={res.summary.var_95} />
            <Stat k="CVaR 95%" v={res.summary.cvar_95} />
            <Stat k="Prob(loss)" v={res.summary.prob_loss} />
            </div>

            <div className="space-y-2">
            <h2 className="text-lg font-semibold">PnL Distribution (Histogram)</h2>
            <PnLHistogramChart
                binEdges={res.histogram.bin_edges}
                counts={res.histogram.counts}
            />
            </div>

            <div className="space-y-2">
            <h2 className="text-lg font-semibold">Sample Path</h2>
            <p className="text-sm text-zinc-600">
                One simulated path showing stock price S(t) and hedge delta(t).
            </p>
            <SamplePathChart
                t={res.sample_path.t}
                S={res.sample_path.S}
                delta={res.sample_path.delta}
            />
            </div>

            <div className="space-y-2">
            <h2 className="text-lg font-semibold">Hedge Positions</h2>
            <p className="text-sm text-zinc-600">
                Evolution of hedge holdings: shares and cash over time.
            </p>
            <HedgePositionChart
                t={res.sample_path.t}
                shares={res.sample_path.shares}
                cash={res.sample_path.cash}
            />
            </div>


            <details>
            <summary className="cursor-pointer text-zinc-700 text-sm">
                Raw JSON
            </summary>
            <pre className="mt-2 overflow-auto rounded-xl bg-zinc-50 p-3 text-xs">
                {JSON.stringify(res, null, 2)}
            </pre>
            </details>
        </section>
        )}

      </div>
    </main>
  );
}

function Stat({ k, v }: { k: string; v: number }) {
  return (
    <div className="rounded-xl border border-zinc-200 p-3">
      <div className="text-xs text-zinc-600">{k}</div>
      <div className="font-mono">{Number.isFinite(v) ? v.toFixed(6) : String(v)}</div>
    </div>
  );
}
