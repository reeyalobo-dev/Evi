import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/shortlists")({
  head: () => ({ meta: [{ title: "Shortlists · EviRank-X" }] }),
  component: () => <ComingSoon title="Shortlists" blurb="Curated top candidates ready for outreach and review." />,
});
