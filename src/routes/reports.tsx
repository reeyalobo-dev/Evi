import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/reports")({
  head: () => ({ meta: [{ title: "Reports · EviRank-X" }] }),
  component: () => <ComingSoon title="Reports" blurb="Print-ready, exportable hiring intelligence reports." />,
});
