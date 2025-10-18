import { Suspense } from "react";

import { CallToAction } from "../components/CallToAction";
import { FeatureList } from "../components/FeatureList";
import { GlassPanel } from "../components/GlassPanel";
import { LogoBadge } from "../components/LogoBadge";
import { SchedulePreview } from "../components/SchedulePreview";
import { getSchedules } from "../lib/api";
import { Schedule } from "../lib/types";

async function SchedulesCard() {
  let schedules: Schedule[] = [];
  try {
    schedules = await getSchedules();
  } catch (error) {
    console.error(error);
  }

  const latestAssignments = schedules[0]?.assignments ?? [];

  return <SchedulePreview assignments={latestAssignments} />;
}

function SchedulesFallback() {
  return (
    <GlassPanel>
      <div className="space-y-4">
        <div className="h-4 w-32 animate-pulse rounded bg-white/20" />
        <div className="space-y-2">
          {[...Array(4).keys()].map((index) => (
            <div key={index} className="h-12 animate-pulse rounded-xl bg-white/10" />
          ))}
        </div>
      </div>
    </GlassPanel>
  );
}

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-12 px-6 py-16 md:flex-row md:items-start md:justify-between">
      <div className="flex-1 space-y-8">
        <LogoBadge />
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl md:text-6xl">
          The radiology duty scheduler that feels like Vite
        </h1>
        <p className="max-w-xl text-lg text-slate-200">
          Fast, opinionated, and effortlessly delightful. Build weekly rosters with drag-and-drop,
          balance capacity automatically, and publish a polished schedule that your team will love.
        </p>
        <CallToAction />
        <GlassPanel>
          <h2 className="text-lg font-semibold text-white">Why teams choose Duty Scheduler</h2>
          <FeatureList />
        </GlassPanel>
      </div>
      <div className="flex w-full max-w-md flex-col gap-6 md:sticky md:top-24">
        <Suspense fallback={<SchedulesFallback />}>
          {/* @ts-expect-error Async Server Component */}
          <SchedulesCard />
        </Suspense>
       <GlassPanel>
          <h3 className="text-lg font-semibold text-white">See it in action</h3>
          <p className="text-sm text-slate-300">
            Connect the API at
            <code className="ml-2 rounded bg-black/40 px-2">
              {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8001"}
            </code>
            to control this preview with live data from your FastAPI backend.
          </p>
        </GlassPanel>
      </div>
    </main>
  );
}
