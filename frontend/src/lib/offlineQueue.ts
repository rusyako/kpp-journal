// Отметки, сделанные без связи. Время фиксируется в момент нажатия и уходит на сервер позже.
import { api, ApiError, OfflineError, type ExitResult } from "./api";

const KEY = "kpp-offline-exits";

export interface QueuedExit {
  student_id: number;
  full_name: string;
  client_time: string;
}

function read(): QueuedExit[] {
  try {
    return JSON.parse(localStorage.getItem(KEY) ?? "[]");
  } catch {
    return [];
  }
}

function write(items: QueuedExit[]): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(items));
  } catch {
    /* хранилище недоступно — очередь живёт до перезагрузки страницы */
  }
}

let memory: QueuedExit[] | null = null;

export function queued(): QueuedExit[] {
  memory ??= read();
  return memory;
}

export function enqueue(item: QueuedExit): void {
  memory = [...queued().filter((q) => q.student_id !== item.student_id), item];
  write(memory);
}

/** Отправить очередь. Возвращает сообщения о том, что не удалось внести. */
export async function flush(): Promise<{ sent: number; failed: string[] }> {
  const failed: string[] = [];
  let sent = 0;
  for (const item of [...queued()]) {
    try {
      await api<ExitResult>("/api/exits", { method: "POST", json: { student_id: item.student_id, client_time: item.client_time } });
      sent++;
    } catch (e) {
      if (e instanceof OfflineError) break; // связи всё ещё нет — попробуем позже
      // 409 «уже отмечен» — тоже снимаем с очереди: выход и так записан
      if (e instanceof ApiError && e.status !== 409) failed.push(`${item.full_name}: ${e.message}`);
    }
    memory = queued().filter((q) => q.student_id !== item.student_id);
    write(memory);
  }
  return { sent, failed };
}
