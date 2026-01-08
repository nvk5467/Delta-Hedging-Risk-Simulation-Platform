"use client";

import React from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  LineChart,
  Line,
  Legend,
} from "recharts";

export function PnLHistogramChart(props: {
  binEdges: number[];
  counts: number[];
}) {
  const { binEdges, counts } = props;

  // counts length is usually binEdges.length - 1
  const n = Math.min(counts.length, Math.max(0, binEdges.length - 1));

  const data = Array.from({ length: n }, (_, i) => {
    const left = binEdges[i];
    const right = binEdges[i + 1];
    return {
      bin: `${left.toFixed(2)} to ${right.toFixed(2)}`,
      mid: (left + right) / 2,
      count: counts[i],
    };
  });

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="mid"
            tickFormatter={(v) => Number(v).toFixed(2)}
            label={{ value: "PnL (bin mid)", position: "insideBottom", offset: -10 }}
          />
          <YAxis label={{ value: "Count", angle: -90, position: "insideLeft" }} />
          <Tooltip
            formatter={(value) => [value, "Count"]}
            labelFormatter={(_, payload) =>
              payload?.[0]?.payload?.bin ? `Bin: ${payload[0].payload.bin}` : ""
            }
          />
          <Bar dataKey="count" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function SamplePathChart(props: {
  t: number[];
  S: number[];
  delta: number[];
}) {
  const { t, S, delta } = props;
  const n = Math.min(t.length, S.length, delta.length);

  const data = Array.from({ length: n }, (_, i) => ({
    t: t[i],
    S: S[i],
    delta: delta[i],
  }));

  

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="t"
            tickFormatter={(v) => Number(v).toFixed(2)}
            label={{ value: "Time (years)", position: "insideBottom", offset: -10 }}
          />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" domain={[0, 1]} />
          <Tooltip />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="S" dot={false} />
          <Line yAxisId="right" type="monotone" dataKey="delta" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function HedgePositionChart(props: {
  t: number[];
  shares: number[];
  cash: number[];
}) {
  const { t, shares, cash } = props;
  const n = Math.min(t.length, shares.length, cash.length);

  const data = Array.from({ length: n }, (_, i) => ({
    t: t[i],
    shares: shares[i],
    cash: cash[i],
  }));

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="t"
            tickFormatter={(v) => Number(v).toFixed(2)}
            label={{ value: "Time (years)", position: "insideBottom", offset: -10 }}
          />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip />
          <Legend />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="shares"
            dot={false}
            name="Shares"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="cash"
            dot={false}
            name="Cash"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

