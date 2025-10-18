const FEATURES = [
  {
    title: "Drag-and-drop scheduling",
    description: "Assign radiologists to shifts quickly while seeing coverage gaps in real time."
  },
  {
    title: "Capacity awareness",
    description: "Honor individual coverage limits and prevent double-bookings before they happen."
  },
  {
    title: "Publish with confidence",
    description: "Share a beautiful, printable schedule snapshot with the team in one click."
  }
];

export function FeatureList() {
  return (
    <div className="grid gap-4">
      {FEATURES.map((feature) => (
        <div key={feature.title} className="rounded-2xl border border-white/10 bg-white/5 p-4 shadow-inner">
          <h3 className="text-lg font-semibold text-white">{feature.title}</h3>
          <p className="text-sm text-slate-300">{feature.description}</p>
        </div>
      ))}
    </div>
  );
}
