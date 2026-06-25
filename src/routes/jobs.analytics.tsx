import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/jobs/analytics")({
  head: () => ({ meta: [{ title: "JD Analytics · EviRank-X" }] }),
  component: () => <ComingSoon title="JD Analytics" blurb="Quality, coverage, and intent signals for every job description." />,
});
