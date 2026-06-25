import { ArrowRight } from "lucide-react";

const CANDIDATES = [
  {
    rank: 1,
    name: "Arjun Mehta",
    exp: "6.2 yrs",
    loc: "Bengaluru",
    score: 0.97,
    confidence: 92,
    skills: ["Retrieval Systems", "Vector DB", "LLMs", "Python", "Evaluation"],
    initial: "AM",
    tone: "from-violet-500 to-fuchsia-500",
  },
  {
    rank: 2,
    name: "Pooja Nair",
    exp: "5.8 yrs",
    loc: "Hyderabad",
    score: 0.96,
    confidence: 89,
    skills: ["RAG", "FAISS", "PyTorch", "MLOps", "Production"],
    initial: "PN",
    tone: "from-cyan-500 to-blue-500",
  },
  {
    rank: 3,
    name: "Rahul Verma",
    exp: "7.1 yrs",
    loc: "Pune",
    score: 0.95,
    confidence: 87,
    skills: ["Milvus", "Embeddings", "Ranking", "Python", "AWS"],
    initial: "RV",
    tone: "from-emerald-500 to-teal-500",
  },
];

export function TopCandidates() {
  return (
    <section className="glass-card rounded-2xl">
      <header className="flex items-center justify-between px-6 py-5">
        <h3 className="font-display text-base font-semibold">
          Top Ranked Candidates{" "}
          <span className="font-normal text-muted-foreground">(ML Engineer - Retrieval)</span>
        </h3>
        <a className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline">
          View Full List <ArrowRight className="size-3.5" />
        </a>
      </header>

      <div className="grid grid-cols-12 gap-3 border-b border-border/60 px-6 pb-2 text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">
        <div className="col-span-1">Rank</div>
        <div className="col-span-3">Candidate</div>
        <div className="col-span-2">Overall Score</div>
        <div className="col-span-4">Key Strengths</div>
        <div className="col-span-2 text-right">Confidence</div>
      </div>

      <ul className="divide-y divide-border/60">
        {CANDIDATES.map((c) => (
          <li
            key={c.name}
            className="grid grid-cols-12 items-center gap-3 px-6 py-4 transition-colors hover:bg-muted/30"
          >
            <div className="col-span-1">
              <span className="grid size-7 place-items-center rounded-lg bg-gradient-brand text-xs font-bold text-white">
                {c.rank}
              </span>
            </div>
            <div className="col-span-3 flex items-center gap-3 min-w-0">
              <div
                className={`grid size-9 shrink-0 place-items-center rounded-full bg-gradient-to-br ${c.tone} text-xs font-semibold text-white`}
              >
                {c.initial}
              </div>
              <div className="min-w-0">
                <div className="truncate text-sm font-semibold">{c.name}</div>
                <div className="truncate text-[11px] text-muted-foreground">
                  {c.exp} · {c.loc}
                </div>
              </div>
            </div>
            <div className="col-span-2">
              <div className="text-sm font-semibold tabular-nums">{c.score.toFixed(2)}</div>
              <div className="mt-1 h-1.5 w-28 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-emerald-300"
                  style={{ width: `${c.score * 100}%` }}
                />
              </div>
            </div>
            <div className="col-span-4 flex flex-wrap gap-1.5">
              {c.skills.map((s) => (
                <span
                  key={s}
                  className="rounded-md border border-border bg-muted/40 px-2 py-0.5 text-[11px] font-medium text-foreground/80"
                >
                  {s}
                </span>
              ))}
            </div>
            <div className="col-span-2 flex items-center justify-end gap-2">
              <span className="text-[12px] font-medium text-emerald-400">High</span>
              <ConfidenceRing value={c.confidence} />
            </div>
          </li>
        ))}
      </ul>

      <div className="border-t border-border/60 px-6 py-3 text-center">
        <a className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline">
          View All Top 100 <ArrowRight className="size-3.5" />
        </a>
      </div>
    </section>
  );
}

function ConfidenceRing({ value }: { value: number }) {
  const r = 16;
  const c = 2 * Math.PI * r;
  const dash = (value / 100) * c;
  return (
    <div className="relative grid size-10 place-items-center">
      <svg viewBox="0 0 40 40" className="size-10 -rotate-90">
        <circle cx="20" cy="20" r={r} stroke="var(--border)" strokeWidth="3" fill="none" />
        <circle
          cx="20"
          cy="20"
          r={r}
          stroke="oklch(0.72 0.18 155)"
          strokeWidth="3"
          strokeLinecap="round"
          fill="none"
          strokeDasharray={`${dash} ${c}`}
        />
      </svg>
      <span className="absolute text-[10px] font-bold tabular-nums">{value}%</span>
    </div>
  );
}