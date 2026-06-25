import { cn } from "@/lib/utils";

export function Logo({ className, size = 36 }: { className?: string; size?: number }) {
  return (
    <div className={cn("flex items-center gap-2.5", className)}>
      <div
        className="relative grid place-items-center rounded-xl bg-gradient-brand glow-ring"
        style={{ width: size, height: size }}
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="white"
          strokeWidth="2.6"
          strokeLinecap="round"
          strokeLinejoin="round"
          style={{ width: size * 0.6, height: size * 0.6 }}
        >
          <path d="M5 4l14 16M19 4L5 20" />
        </svg>
      </div>
      <div className="flex flex-col leading-none">
        <span className="font-display text-[15px] font-semibold tracking-tight">
          EviRank<span className="text-gradient-brand">-X</span>
        </span>
        <span className="mt-0.5 text-[10px] font-medium uppercase tracking-[0.14em] text-muted-foreground">
          Evidence · Ranked
        </span>
      </div>
    </div>
  );
}