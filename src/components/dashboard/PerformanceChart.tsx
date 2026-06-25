import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const DATA = [
  { d: "May 8", v: 0.74 },
  { d: "May 9", v: 0.83 },
  { d: "May 10", v: 0.78 },
  { d: "May 11", v: 0.85 },
  { d: "May 12", v: 0.79 },
  { d: "May 13", v: 0.88 },
  { d: "May 14", v: 0.865 },
];

export function PerformanceChart() {
  return (
    <section className="glass-card rounded-2xl p-6">
      <header className="mb-4 flex items-center justify-between">
        <h3 className="font-display text-base font-semibold">
          Ranking Performance <span className="text-muted-foreground">(NDCG@10)</span>
        </h3>
        <button className="rounded-lg border border-border bg-muted/40 px-2.5 py-1 text-[11px] font-medium text-muted-foreground hover:bg-muted">
          Last 7 Days ▾
        </button>
      </header>
      <div className="h-[200px] w-full">
        <ResponsiveContainer>
          <AreaChart data={DATA} margin={{ top: 10, right: 10, left: -16, bottom: 0 }}>
            <defs>
              <linearGradient id="ndcgFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="oklch(0.68 0.22 285)" stopOpacity={0.45} />
                <stop offset="100%" stopColor="oklch(0.68 0.22 285)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="d"
              stroke="currentColor"
              tick={{ fontSize: 11, fill: "var(--muted-foreground)" }}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              domain={[0, 1]}
              ticks={[0, 0.2, 0.4, 0.6, 0.8, 1]}
              tick={{ fontSize: 11, fill: "var(--muted-foreground)" }}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              contentStyle={{
                background: "var(--popover)",
                border: "1px solid var(--border)",
                borderRadius: 10,
                fontSize: 12,
              }}
              labelStyle={{ color: "var(--muted-foreground)" }}
              cursor={{ stroke: "var(--primary)", strokeOpacity: 0.3 }}
            />
            <Area
              type="monotone"
              dataKey="v"
              stroke="oklch(0.78 0.18 285)"
              strokeWidth={2.5}
              fill="url(#ndcgFill)"
              dot={{ r: 4, fill: "oklch(0.78 0.18 285)", strokeWidth: 0 }}
              activeDot={{ r: 6 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}