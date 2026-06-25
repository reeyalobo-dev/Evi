import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/analytics")({
  head: () => ({ meta: [{ title: "Analytics · EviRank-X" }] }),
  component: () => <ComingSoon title="Analytics" blurb="NDCG, MAP, precision, latency, and diversity metrics." />,
});
