import { Schedule } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8001";

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    next: { revalidate: 0 }
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch ${path}: ${res.statusText}`);
  }

  return res.json();
}

export async function getSchedules(): Promise<Schedule[]> {
  return fetchJson<Schedule[]>("/api/schedules");
}
