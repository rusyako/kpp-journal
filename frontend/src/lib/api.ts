import { initData } from "./telegram";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

/** Нет связи с сервером (в отличие от ответа с ошибкой). */
export class OfflineError extends Error {}

export function api(path: string, options: RequestInit & { responseType: "blob" }): Promise<Blob>;
export function api<T>(path: string, options?: RequestInit & { json?: unknown }): Promise<T>;
export async function api<T>(path: string, options: RequestInit & { json?: unknown; responseType?: "blob" } = {}): Promise<T | Blob> {
  const { json, responseType, ...requestOptions } = options;
  const headers = new Headers(options.headers);
  const tg = initData();
  if (tg) headers.set("X-Telegram-Init-Data", tg);
  let body = options.body;
  if (json !== undefined) {
    headers.set("Content-Type", "application/json");
    body = JSON.stringify(json);
  }
  let res: Response;
  try {
    res = await fetch(path, { ...requestOptions, headers, body, credentials: "same-origin" });
  } catch {
    throw new OfflineError("Нет связи с сервером");
  }
  if (!res.ok) {
    let message = res.statusText;
    try {
      const data = await res.json();
      if (typeof data.detail === "string") message = data.detail;
    } catch {
      /* не JSON */
    }
    throw new ApiError(res.status, message);
  }
  return responseType === "blob" ? res.blob() : res.json() as Promise<T>;
}

// ---- Типы ответов API ----

export type Role = "admin" | "guard" | "advisor" | "viewer";

export interface Me {
  id: number;
  role: Role;
  display_name: string;
  advisories: { id: number; name: string }[];
  today: string;
  working_day: boolean;
}

export type RowStatus = "none" | "allowed" | "ok" | "early" | "no_permission";

export interface DayRow {
  student_id: number;
  full_name: string;
  class_name: string;
  advisory: string;
  advisory_id: number;
  allowed_time: string | null;
  reason: string;
  exited: boolean;
  exit_time: string | null;
  exit_offline: boolean;
  status: RowStatus;
  color: "" | "yellow" | "green" | "orange";
}

export interface Day {
  date: string;
  today: string;
  working_day: boolean;
  rows: DayRow[];
}

export interface ExitResult {
  message: string;
  status: RowStatus;
  row: DayRow;
}

export interface AdvisorRow {
  student_id: number;
  full_name: string;
  class_name: string;
  time: string;
  reason: string;
  status: string;
  exit: string;
  early: boolean;
  color: "" | "yellow" | "green";
}

export interface AdvisoryView {
  id: number;
  name: string;
  editable: boolean;
  rows: AdvisorRow[];
}

export const formatDate = (iso: string) => iso.split("-").reverse().join(".");
