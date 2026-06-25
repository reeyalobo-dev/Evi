import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/engine")({
  head: () => ({ meta: [{ title: "EviRank-X Engine · EviRank-X" }] }),
  component: () => <ComingSoon title="EviRank-X Engine" blurb="Live status, model versions, and pipeline diagnostics." />,
});
