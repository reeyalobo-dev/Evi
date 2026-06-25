import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/compare")({
  head: () => ({ meta: [{ title: "Candidate Compare · EviRank-X" }] }),
  component: () => <ComingSoon title="Candidate Compare" blurb="Side-by-side evidence, decision trace, and AI recommendation." />,
});
