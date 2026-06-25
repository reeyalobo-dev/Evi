import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/explainability")({
  head: () => ({ meta: [{ title: "Explainability · EviRank-X" }] }),
  component: () => <ComingSoon title="Explainability" blurb="SHAP, feature importance, and natural-language explanations." />,
});
