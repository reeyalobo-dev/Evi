import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/jobs/new")({
  head: () => ({ meta: [{ title: "Create New JD · EviRank-X" }] }),
  component: () => <ComingSoon title="Create New JD" blurb="Draft a job description with AI-assisted hiring intent extraction." />,
});
