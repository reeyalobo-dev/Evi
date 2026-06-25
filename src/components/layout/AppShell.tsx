import { type ReactNode, useState } from "react";
import { Link, useRouterState } from "@tanstack/react-router";
import { motion } from "framer-motion";
import {
  Bell,
  HelpCircle,
  Search,
  Sun,
  Moon,
  Plus,
  Play,
  LayoutDashboard,
  FileText,
  Sparkles,
  BookOpen,
  Users,
  Trophy,
  GitCompareArrows,
  BarChart3,
  Eye,
  ScrollText,
  Settings,
  ChevronDown,
  Bookmark,
  Cpu,
} from "lucide-react";
import { Logo } from "@/components/brand/Logo";
import { cn } from "@/lib/utils";

type NavItem = { to: string; label: string; icon: typeof LayoutDashboard; badge?: string };
type NavGroup = { label: string; items: NavItem[] };

const NAV: NavGroup[] = [
  {
    label: "Overview",
    items: [{ to: "/", label: "Dashboard", icon: LayoutDashboard }],
  },
  {
    label: "Hiring Intelligence",
    items: [
      { to: "/jobs", label: "Job Descriptions", icon: FileText },
      { to: "/jobs/new", label: "Create New JD", icon: Plus },
      { to: "/jobs/analytics", label: "JD Analytics", icon: BarChart3 },
    ],
  },
  {
    label: "Candidates",
    items: [
      { to: "/candidates", label: "Search Candidates", icon: Search },
      { to: "/candidates/all", label: "All Candidates", icon: Users },
      { to: "/shortlists", label: "Shortlists", icon: Bookmark },
    ],
  },
  {
    label: "AI Ranking",
    items: [
      { to: "/rankings", label: "Rankings", icon: Trophy, badge: "New" },
      { to: "/engine", label: "EviRank-X Engine", icon: Cpu },
      { to: "/compare", label: "Candidate Compare", icon: GitCompareArrows },
    ],
  },
  {
    label: "Insights",
    items: [
      { to: "/analytics", label: "Analytics", icon: BarChart3 },
      { to: "/explainability", label: "Explainability", icon: Eye },
      { to: "/reports", label: "Reports", icon: ScrollText },
    ],
  },
];

export function AppShell({ children }: { children: ReactNode }) {
  const [dark, setDark] = useState(true);

  const toggleTheme = () => {
    const html = document.documentElement;
    html.classList.toggle("dark");
    setDark(html.classList.contains("dark"));
  };

  return (
    <div className="relative flex min-h-screen w-full bg-background text-foreground">
      {/* Ambient glow */}
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 -z-10"
        style={{ backgroundImage: "var(--gradient-glow)" }}
      />
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopNav dark={dark} onToggleTheme={toggleTheme} />
        <main className="min-w-0 flex-1 p-6 lg:p-8">{children}</main>
      </div>
    </div>
  );
}

function Sidebar() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <aside className="sticky top-0 hidden h-screen w-[260px] shrink-0 flex-col border-r border-sidebar-border bg-sidebar/80 backdrop-blur-xl lg:flex">
      <div className="px-5 py-5">
        <Logo />
      </div>

      <nav className="flex-1 overflow-y-auto px-3 pb-4">
        {NAV.map((group) => (
          <div key={group.label} className="mb-5">
            <div className="px-3 pb-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground/70">
              {group.label}
            </div>
            <ul className="space-y-0.5">
              {group.items.map((item) => {
                const active = item.to === "/" ? pathname === "/" : pathname.startsWith(item.to);
                return (
                  <li key={item.to}>
                    <Link
                      to={item.to}
                      className={cn(
                        "group relative flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all",
                        active
                          ? "bg-sidebar-accent text-sidebar-accent-foreground shadow-[inset_0_0_0_1px_color-mix(in_oklab,var(--primary)_30%,transparent)]"
                          : "text-muted-foreground hover:bg-sidebar-accent/40 hover:text-foreground",
                      )}
                    >
                      {active && (
                        <motion.span
                          layoutId="sidebar-active"
                          className="absolute left-0 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-r-full bg-gradient-brand"
                          transition={{ type: "spring", stiffness: 380, damping: 30 }}
                        />
                      )}
                      <item.icon className="size-[18px] shrink-0 opacity-80" />
                      <span className="flex-1 truncate">{item.label}</span>
                      {item.badge && (
                        <span className="rounded-md bg-gradient-brand px-1.5 py-0.5 text-[10px] font-semibold text-white">
                          {item.badge}
                        </span>
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* Engine status */}
      <div className="mx-3 mb-3 rounded-xl border border-sidebar-border bg-card/60 p-3.5">
        <div className="flex items-center justify-between">
          <div className="text-xs font-semibold">EviRank-X Engine</div>
          <div className="flex items-center gap-1.5 text-[11px] font-medium text-emerald-400">
            <span className="relative grid place-items-center">
              <span className="absolute size-2 animate-ping rounded-full bg-emerald-400/60" />
              <span className="relative size-1.5 rounded-full bg-emerald-400" />
            </span>
            Active
          </div>
        </div>
        <div className="mt-2 space-y-0.5 text-[11px] text-muted-foreground">
          <div>Model: BGE-Reranker v2</div>
          <div>Updated: Today, 09:15 AM</div>
        </div>
        <button className="mt-2.5 text-[11px] font-medium text-primary hover:underline">
          View Engine Details →
        </button>
      </div>

      <div className="flex items-center gap-3 border-t border-sidebar-border p-3">
        <div className="grid size-9 place-items-center rounded-full bg-gradient-brand text-sm font-semibold text-white">
          AS
        </div>
        <div className="min-w-0 flex-1">
          <div className="truncate text-sm font-medium">Ananya Sharma</div>
          <div className="truncate text-[11px] text-muted-foreground">Talent Partner</div>
        </div>
        <ChevronDown className="size-4 text-muted-foreground" />
      </div>
    </aside>
  );
}

function TopNav({ dark, onToggleTheme }: { dark: boolean; onToggleTheme: () => void }) {
  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b border-border/60 bg-background/70 px-6 backdrop-blur-xl">
      <div className="relative flex-1 max-w-2xl">
        <Search className="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          placeholder="Search candidates, jobs, skills, evidence…"
          className="h-10 w-full rounded-xl border border-border bg-muted/40 pl-10 pr-20 text-sm placeholder:text-muted-foreground focus:border-primary/50 focus:bg-card focus:outline-none focus:ring-2 focus:ring-primary/20"
        />
        <kbd className="absolute right-3 top-1/2 hidden -translate-y-1/2 items-center gap-1 rounded-md border border-border bg-card px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground md:inline-flex">
          ⌘K
        </kbd>
      </div>

      <div className="flex items-center gap-1.5">
        <button className="relative grid size-9 place-items-center rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground">
          <Bell className="size-[18px]" />
          <span className="absolute right-1.5 top-1.5 grid size-4 place-items-center rounded-full bg-destructive text-[9px] font-bold text-white">
            12
          </span>
        </button>
        <button className="grid size-9 place-items-center rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground">
          <HelpCircle className="size-[18px]" />
        </button>
        <button
          onClick={onToggleTheme}
          className="grid size-9 place-items-center rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground"
          aria-label="Toggle theme"
        >
          {dark ? <Sun className="size-[18px]" /> : <Moon className="size-[18px]" />}
        </button>
      </div>
    </header>
  );
}

export function PageHeader({
  greeting,
  subtitle,
  actions,
}: {
  greeting: ReactNode;
  subtitle: string;
  actions?: ReactNode;
}) {
  return (
    <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight md:text-[28px]">
          {greeting}
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
      </div>
      {actions && <div className="flex flex-wrap items-center gap-2.5">{actions}</div>}
    </div>
  );
}

export function PrimaryButton({
  children,
  icon: Icon = Play,
}: {
  children: ReactNode;
  icon?: typeof Play;
}) {
  return (
    <button className="group inline-flex h-10 items-center gap-2 rounded-xl bg-gradient-brand px-4 text-sm font-semibold text-white shadow-[0_8px_24px_-8px_color-mix(in_oklab,var(--primary)_60%,transparent)] transition-transform hover:-translate-y-0.5">
      <Icon className="size-4" />
      {children}
    </button>
  );
}

export function SecondaryButton({
  children,
  icon: Icon,
}: {
  children: ReactNode;
  icon?: typeof Plus;
}) {
  return (
    <button className="inline-flex h-10 items-center gap-2 rounded-xl border border-border bg-card/60 px-4 text-sm font-medium text-foreground transition-colors hover:border-primary/40 hover:bg-card">
      {Icon && <Icon className="size-4" />}
      {children}
    </button>
  );
}

export { Sparkles, BookOpen };