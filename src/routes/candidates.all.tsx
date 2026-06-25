import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/candidates/all")({
  head: () => ({ meta: [{ title: "All Candidates · EviRank-X" }] }),
  component: () => <ComingSoon title="All Candidates" blurb="The complete enriched candidate intelligence database." />,
});
