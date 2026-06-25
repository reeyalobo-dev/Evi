import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import { ArrowRight } from "lucide-react";

const DATA = [
  { name: "Semantic Evidence", value: 38, color: "oklch(0.7 0.2 285)" },
  { name: "Career Evidence", value: 22, color: "oklch(0.72 0.16 220)" },
  { name: "Project Evidence", value: 20, color: "oklch(0.78 0.14 200)" },
  { name: "Behavior Evidence", value: 12, color: "oklch(0.78 0.17 75)" },
  { name: "Constraint Evidence", value: 8, color: "oklch(0.72 0.18 155)" },
];

export function EvidenceBreakdown() {
  return (
    <section className="glass-card rounded-2xl p-6">
      <header className="mb-4 flex items-center justify-between">
        <h3 className="font-display text-base font-semibold">
          Evidence Breakdown <span className="text-muted-foreground">(Top Candidate)</span>
        </h3>
        <a className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline">
          View Explanation <ArrowRight className="size-3.5" />
        </a>
      </header>

      <div className="flex items-center gap-6">
        <div className="relative size-[160px] shrink-0">
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={DATA}
                dataKey="value"
                innerRadius={52}
                outerRadius={78}
                paddingAngle={2}
                stroke="none"
              >
                {DATA.map((d) => (
                  <Cell key={d.name} fill={d.color} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          <div className="pointer-events-none absolute inset-0 grid place-items-center">
            <div className="text-center">
              <div className="font-display text-2xl font-semibold tabular-nums">0.97</div>
              <div className="text-[10px] uppercase tracking-[0.12em] text-muted-foreground">
                Overall Score
              </div>
            </div>
          </div>
        </div>

        <ul className="flex-1 space-y-2.5 text-sm">
          {DATA.map((d) => (
            <li key={d.name} className="flex items-center justify-between gap-3">
              <span className="flex items-center gap-2.5">
                <span className="size-2.5 rounded-full" style={{ background: d.color }} />
                <span className="text-foreground/90">{d.name}</span>
              </span>
              <span className="font-semibold tabular-nums">{d.value}%</span>
            </li>
          ))}
        </ul>
      </div>
      <p className="mt-4 text-[11px] text-muted-foreground">
        Evidence scores are normalized contributions from the Adaptive Evidence Fusion layer.
      </p>
    </section>
  );
}