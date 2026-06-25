import { motion } from "framer-motion";
import { ArrowDown, ArrowUp, type LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

type Tone = "violet" | "cyan" | "emerald" | "amber" | "rose";

const TONE: Record<Tone, { bg: string; text: string }> = {
  violet: { bg: "bg-[color-mix(in_oklab,var(--violet)_18%,transparent)]", text: "text-[color:var(--violet)]" },
  cyan: { bg: "bg-[color-mix(in_oklab,var(--cyan)_18%,transparent)]", text: "text-[color:var(--cyan)]" },
  emerald: { bg: "bg-[color-mix(in_oklab,var(--emerald)_18%,transparent)]", text: "text-[color:var(--emerald)]" },
  amber: { bg: "bg-[color-mix(in_oklab,var(--amber)_18%,transparent)]", text: "text-[color:var(--amber)]" },
  rose: { bg: "bg-[color-mix(in_oklab,var(--destructive)_18%,transparent)]", text: "text-[color:var(--destructive)]" },
};

export function StatCard({
  label,
  value,
  delta,
  deltaLabel = "vs last month",
  icon: Icon,
  tone,
  index = 0,
}: {
  label: string;
  value: string;
  delta: number;
  deltaLabel?: string;
  icon: LucideIcon;
  tone: Tone;
  index?: number;
}) {
  const up = delta >= 0;
  const t = TONE[tone];
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.4, ease: "easeOut" }}
      className="glass-card relative overflow-hidden rounded-2xl p-5"
    >
      <div className="flex items-start gap-4">
        <div className={cn("grid size-12 shrink-0 place-items-center rounded-xl", t.bg)}>
          <Icon className={cn("size-5", t.text)} />
        </div>
        <div className="min-w-0 flex-1">
          <div className="text-[12px] font-medium text-muted-foreground">{label}</div>
          <div className="mt-1 font-display text-[26px] font-semibold leading-tight tracking-tight">
            {value}
          </div>
          <div className="mt-1.5 flex items-center gap-1 text-[11px]">
            <span
              className={cn(
                "inline-flex items-center gap-0.5 font-semibold",
                up ? "text-emerald-400" : "text-rose-400",
              )}
            >
              {up ? <ArrowUp className="size-3" /> : <ArrowDown className="size-3" />}
              {Math.abs(delta)}%
            </span>
            <span className="text-muted-foreground">{deltaLabel}</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}