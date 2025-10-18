import type { PropsWithChildren } from "react";

export function GlassPanel({ children }: PropsWithChildren) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/10 p-6 shadow-xl shadow-black/30 backdrop-blur">
      {children}
    </div>
  );
}
