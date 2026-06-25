import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/candidates")({
  head: () => ({ meta: [{ title: "Search Candidates · EviRank-X" }] }),
  component: () => <ComingSoon title="Search Candidates" blurb="Natural-language and semantic search across your talent graph." />,
});
