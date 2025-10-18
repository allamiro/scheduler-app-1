import { format, parseISO } from "date-fns";

import { Assignment } from "../lib/types";
import { GlassPanel } from "./GlassPanel";

function AssignmentRow({ assignment }: { assignment: Assignment }) {
  return (
    <div className="flex items-center justify-between rounded-xl bg-white/5 px-3 py-2 text-sm text-slate-200">
      <div>
        <p className="font-semibold text-white">{assignment.doctor.name}</p>
        <p className="text-xs text-slate-300">{assignment.doctor.specialty}</p>
      </div>
      <div className="text-right">
        <p className="font-medium text-brand-accent">{assignment.assignment_type}</p>
        <p className="text-xs text-slate-400">{format(parseISO(assignment.date), "eee, MMM d")}</p>
      </div>
    </div>
  );
}

export function SchedulePreview({ assignments }: { assignments: Assignment[] }) {
  return (
    <GlassPanel>
      <div className="space-y-4">
        <header className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">This week&apos;s coverage</h3>
          <span className="rounded-full bg-brand/20 px-3 py-1 text-xs font-semibold text-brand">Live</span>
        </header>
        <div className="space-y-2">
          {assignments.slice(0, 4).map((assignment) => (
            <AssignmentRow key={assignment.id} assignment={assignment} />
          ))}
          {assignments.length === 0 && (
            <p className="text-sm text-slate-300">No assignments yet. Create your first schedule to see it here.</p>
          )}
        </div>
      </div>
    </GlassPanel>
  );
}
