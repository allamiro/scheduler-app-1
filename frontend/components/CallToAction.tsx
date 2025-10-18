import Link from "next/link";

export function CallToAction() {
  return (
    <div className="flex flex-wrap items-center gap-4">
      <Link
        href="/app"
        className="rounded-full bg-brand px-6 py-3 text-sm font-semibold text-slate-950 shadow-lg shadow-brand/30 transition hover:-translate-y-0.5 hover:bg-brand-accent"
      >
        Launch scheduler
      </Link>
      <Link
        href="https://github.com/allamiro/scheduler-app"
        className="rounded-full border border-white/30 px-6 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:border-white/60"
      >
        View API docs
      </Link>
    </div>
  );
}
