import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Sparkles } from "lucide-react";

export function ComingSoon({ title, blurb }: { title: string; blurb: string }) {
  return (
    <AppShell>
      <PageHeader greeting={title} subtitle={blurb} />
      <div className="glass-card grid place-items-center rounded-2xl p-16 text-center">
        <div className="grid size-14 place-items-center rounded-2xl bg-gradient-brand glow-ring">
          <Sparkles className="size-6 text-white" />
        </div>
        <h3 className="mt-5 font-display text-xl font-semibold">Module in development</h3>
        <p className="mt-2 max-w-md text-sm text-muted-foreground">
          This workspace is part of the EviRank-X intelligence suite. Connect your data sources
          to unlock the full experience.
        </p>
      </div>
    </AppShell>
  );
}
