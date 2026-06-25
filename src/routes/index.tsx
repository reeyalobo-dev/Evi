import { createFileRoute } from "@tanstack/react-router";
import { BarChart3, Plus, Target, Timer, TrendingUp, Users, Play } from "lucide-react";
import { AppShell, PageHeader, PrimaryButton, SecondaryButton } from "@/components/layout/AppShell";
import { StatCard } from "@/components/dashboard/StatCard";
import { RecentRankings } from "@/components/dashboard/RecentRankings";
import { EnginePipeline } from "@/components/dashboard/EnginePipeline";
import { PerformanceChart } from "@/components/dashboard/PerformanceChart";
import { EvidenceBreakdown } from "@/components/dashboard/EvidenceBreakdown";
import { TopCandidates } from "@/components/dashboard/TopCandidates";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Dashboard · EviRank-X" },
      { name: "description", content: "AI-powered recruitment intelligence dashboard. Track rankings, evidence quality, and engine performance." },
      { property: "og:title", content: "Dashboard · EviRank-X" },
      { property: "og:description", content: "Adaptive Evidence Fusion Ranking — explainable AI for enterprise hiring." },
    ],
  }),
  component: Dashboard,
});

function Dashboard() {
  return (
    <AppShell>
      <PageHeader
        greeting={
          <>
            Welcome back, <span className="text-gradient-brand">Ananya</span>{" "}
            <span className="inline-block">👋</span>
          </>
        }
        subtitle="AI-Powered recruitment. Smarter rankings. Better hires."
        actions={
          <>
            <SecondaryButton icon={Plus}>Create New JD</SecondaryButton>
            <PrimaryButton icon={Play}>Run New Ranking</PrimaryButton>
          </>
        }
      />

      {/* Stat row */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        <StatCard label="Active Jobs" value="24" delta={20} icon={BarChart3} tone="violet" index={0} />
        <StatCard label="Candidates Ranked" value="128.7K" delta={32} icon={Users} tone="cyan" index={1} />
        <StatCard label="Top 100 Shortlists" value="432" delta={18} icon={Target} tone="emerald" index={2} />
        <StatCard label="Avg. NDCG@10" value="0.865" delta={7} icon={TrendingUp} tone="amber" index={3} />
        <StatCard label="Avg. Ranking Time" value="42s" delta={-18} deltaLabel="vs last month" icon={Timer} tone="cyan" index={4} />
      </div>

      {/* Main grid */}
      <div className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div className="space-y-6 xl:col-span-2">
          <RecentRankings />
          <TopCandidates />
        </div>
        <div className="space-y-6">
          <EnginePipeline />
          <PerformanceChart />
          <EvidenceBreakdown />
        </div>
      </div>
    </AppShell>
  );
}
