import { createFileRoute } from "@tanstack/react-router";
import { ComingSoon } from "@/components/layout/ComingSoon";

export const Route = createFileRoute("/jobs")({
  head: () => ({ meta: [{ title: "Job Descriptions · EviRank-X" }] }),
  component: () => <ComingSoon title="Job Descriptions" blurb="Manage, version, and analyze every JD across your pipeline." />,
});
