import { motion } from "framer-motion";
import { FileText, Layers, Search, BarChart3, ShieldCheck, Trophy, ArrowRight } from "lucide-react";

const STEPS = [
  { icon: FileText, label: "Intent Engine" },
  { icon: Layers, label: "Evidence Builder" },
  { icon: Search, label: "Hybrid Retrieval" },
  { icon: BarChart3, label: "LTR Ranker" },
  { icon: ShieldCheck, label: "Verification" },
  { icon: Trophy, label: "Top 100" },
];

export function EnginePipeline() {
  return (
    <section className="glass-card rounded-2xl p-6">
      <header className="mb-5 flex items-center justify-between">
        <h3 className="font-display text-base font-semibold">EviRank-X Engine Overview</h3>
        <a className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline">
          View Details <ArrowRight className="size-3.5" />
        </a>
      </header>

      <div className="flex items-center justify-between gap-1.5">
        {STEPS.map((s, i) => (
          <div key={s.label} className="flex flex-1 items-center">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              className="flex flex-1 flex-col items-center gap-2 text-center"
            >
              <div className="grid size-10 place-items-center rounded-xl border border-border bg-muted/40">
                <s.icon className="size-[18px] text-[color:var(--primary)]" />
              </div>
              <div className="text-[10px] font-medium leading-tight text-muted-foreground">
                {s.label}
              </div>
            </motion.div>
            {i < STEPS.length - 1 && (
              <div className="relative -mt-4 h-px flex-1 bg-gradient-to-r from-border via-primary/40 to-border">
                <motion.span
                  className="absolute inset-y-0 -top-px h-[2px] w-6 rounded-full bg-gradient-brand"
                  initial={{ x: 0, opacity: 0 }}
                  animate={{ x: ["0%", "300%"], opacity: [0, 1, 0] }}
                  transition={{ duration: 2.2, repeat: Infinity, delay: i * 0.3, ease: "easeInOut" }}
                />
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 grid grid-cols-2 gap-3 rounded-xl border border-border bg-muted/20 p-4 sm:grid-cols-4">
        <Meta label="Model Status" value="Active" valueClass="text-emerald-400" />
        <Meta label="Last Trained" value="Today, 02:15 AM" />
        <Meta label="Training Data" value="250K pairs" />
        <Meta label="Teacher Model" value="bge-reranker-v2" />
      </div>
    </section>
  );
}

function Meta({ label, value, valueClass = "" }: { label: string; value: string; valueClass?: string }) {
  return (
    <div>
      <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">
        {label}
      </div>
      <div className={`mt-1 text-[13px] font-semibold tabular-nums ${valueClass}`}>{value}</div>
    </div>
  );
}