import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/rankings")({
  head: () => ({ meta: [{ title: "Rankings · EviRank-X" }] }),
  component: () => <ComingSoon title="Rankings" blurb="Adaptive Evidence Fusion rankings with full decision traces." />,
});
