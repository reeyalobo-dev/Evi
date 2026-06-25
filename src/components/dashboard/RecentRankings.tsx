import { ArrowRight, CheckCircle2 } from "lucide-react";

const ROWS = [
  { title: "ML Engineer - Retrieval", cand: "12,842", top: 0.97, ndcg: 0.892, date: "May 14, 2025", time: "09:20 AM" },
  { title: "Senior AI Engineer", cand: "8,753", top: 0.96, ndcg: 0.878, date: "May 13, 2025", time: "06:15 PM" },
  { title: "Data Scientist", cand: "15,671", top: 0.94, ndcg: 0.841, date: "May 13, 2025", time: "11:40 AM" },
  { title: "MLOps Engineer", cand: "9,102", top: 0.93, ndcg: 0.826, date: "May 12, 2025", time: "08:30 PM" },
  { title: "AI Platform Engineer", cand: "7,256", top: 0.94, ndcg: 0.835, date: "May 12, 2025", time: "02:10 PM" },
];

export function RecentRankings() {
  return (
    <section className="glass-card rounded-2xl">
      <header className="flex items-center justify-between px-6 py-5">
        <h3 className="font-display text-base font-semibold">Recent Rankings</h3>
        <a className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline">
          View All Rankings <ArrowRight className="size-3.5" />
        </a>
      </header>

      <div className="grid grid-cols-12 gap-3 border-b border-border/60 px-6 pb-2 text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">
        <div className="col-span-4">Job Title</div>
        <div className="col-span-2 text-right">Candidates</div>
        <div className="col-span-1 text-right">Top</div>
        <div className="col-span-1 text-right">NDCG@10</div>
        <div className="col-span-2">Status</div>
        <div className="col-span-2">Date</div>
      </div>

      <ul className="divide-y divide-border/60">
        {ROWS.map((r) => (
          <li
            key={r.title}
            className="group grid grid-cols-12 items-center gap-3 px-6 py-3.5 text-sm transition-colors hover:bg-muted/30"
          >
            <div className="col-span-4 min-w-0">
              <div className="truncate font-medium">{r.title}</div>
              <div className="text-[11px] text-muted-foreground">EviRank-X</div>
            </div>
            <div className="col-span-2 text-right tabular-nums text-muted-foreground">{r.cand}</div>
            <div className="col-span-1 text-right">
              <span className="inline-block rounded-md bg-emerald-500/10 px-2 py-0.5 text-[11px] font-semibold tabular-nums text-emerald-400">
                {r.top.toFixed(2)}
              </span>
            </div>
            <div className="col-span-1 text-right">
              <span className="inline-block rounded-md bg-[color-mix(in_oklab,var(--primary)_15%,transparent)] px-2 py-0.5 text-[11px] font-semibold tabular-nums text-[color:var(--primary)]">
                {r.ndcg.toFixed(3)}
              </span>
            </div>
            <div className="col-span-2">
              <span className="inline-flex items-center gap-1.5 text-[12px] font-medium text-emerald-400">
                <CheckCircle2 className="size-3.5" /> Completed
              </span>
            </div>
            <div className="col-span-2 text-[12px] text-muted-foreground">
              <div>{r.date}</div>
              <div className="text-[11px] opacity-70">{r.time}</div>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}