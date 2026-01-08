"use client";

import { useState } from "react";
import { api, GreeksRes } from "@/lib/api";

function NumInput(props: {
  value: number;
  onChange: (v: number) => void;
  step?: number;
  min?: number;
}) {
  return (
    <input
      type="number"
      className="w-full rounded-xl border border-zinc-300 px-3 py-2 text-sm"
      value={Number.isFinite(props.value) ? props.value : ""}
      step={props.step ?? 0.01}
      min={props.min}
      onChange={(e) => props.onChange(Number(e.target.value))}
    />
  );
}

function KV({ k, v }: { k: string; v: number }) {
  return (
    <div className="rounded-xl border border-zinc-200 p-3">
      <div className="text-xs text-zinc-600">{k}</div>
      <div className="font-mono">{v.toFixed(6)}</div>
    </div>
  );
}

export default function Home() {
  const [S0, setS0] = useState(100);
  const [K, setK] = useState(100);
  const [r, setR] = useState(0.05);
  const [sigma, setSigma] = useState(0.2);
  const [T, setT] = useState(1.0);
  const [optionType, setOptionType] = useState<"call" | "put">("call");

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [res, setRes] = useState<GreeksRes | null>(null);

  async function run() {
    setLoading(true);
    setErr(null);
    setRes(null);
    try {
      const out = await api.greeks({
        S0,
        K,
        r,
        sigma,
        T,
        option_type: optionType,
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
        <header className="space-y-1">
          <h1 className="text-2xl font-bold">Black-Scholes Greeks</h1>
          <p className="text-sm text-zinc-600">
            Calls your backend endpoint: <code>/api/greeks</code>
          </p>
        </header>

        <section className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
          <div className="grid gap-3">
            <Row label="S0">
              <NumInput value={S0} onChange={setS0} min={0} />
            </Row>
            <Row label="K">
              <NumInput value={K} onChange={setK} min={0} />
            </Row>
            <Row label="r">
              <NumInput value={r} onChange={setR} step={0.005} />
            </Row>
            <Row label="sigma">
              <NumInput value={sigma} onChange={setSigma} step={0.01} min={0} />
            </Row>
            <Row label="T (years)">
              <NumInput value={T} onChange={setT} step={0.05} min={0} />
            </Row>
            <Row label="type">
              <select
                className="w-full rounded-xl border border-zinc-300 px-3 py-2 text-sm"
                value={optionType}
                onChange={(e) => setOptionType(e.target.value as "call" | "put")}
              >
                <option value="call">call</option>
                <option value="put">put</option>
              </select>
            </Row>

            <button
              onClick={run}
              disabled={loading}
              className="mt-2 w-full rounded-xl bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
            >
              {loading ? "Calculating..." : "Calculate"}
            </button>

            {err && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-800">
                {err}
              </div>
            )}
          </div>
        </section>

        <section className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
          <h2 className="mb-3 text-lg font-semibold">Result</h2>

          {!res ? (
            <p className="text-sm text-zinc-600">Run a calculation.</p>
          ) : (
            <div className="space-y-3 text-sm">
              <div>
                <span className="font-medium">Price:</span>{" "}
                {res.price.toFixed(6)}
              </div>

              <div className="grid grid-cols-2 gap-2">
                <KV k="Delta" v={res.greeks.delta} />
                <KV k="Gamma" v={res.greeks.gamma} />
                <KV k="Theta (per year)" v={res.greeks.theta} />
                <KV k="Vega (per 1.0 vol)" v={res.greeks.vega} />
                <KV k="Rho (per 1.0 rate)" v={res.greeks.rho} />
              </div>

              <details>
                <summary className="cursor-pointer text-zinc-700">
                  Raw JSON
                </summary>
                <pre className="mt-2 overflow-auto rounded-xl bg-zinc-50 p-3 text-xs">
                  {JSON.stringify(res, null, 2)}
                </pre>
              </details>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

function Row({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <label className="grid grid-cols-3 items-center gap-3">
      <span className="text-sm text-zinc-700">{label}</span>
      <div className="col-span-2">{children}</div>
    </label>
  );
}
