import { useCallback, useEffect, useMemo, useRef, useState, type KeyboardEvent } from "react";
import { TopBar, useMe } from "../App";
import { api, ApiError, formatDate, OfflineError, type Day, type DayRow, type ExitResult, type RowStatus } from "../lib/api";
import { useLiveUpdates } from "../lib/live";
import { enqueue, flush, queued } from "../lib/offlineQueue";
import { search } from "../lib/search";

const DAY_CACHE = "kpp-day";

type BannerKind = "ok" | "early" | "warn" | "info";

const BANNER_KIND: Record<RowStatus, BannerKind> = {
  ok: "ok",
  early: "early",
  no_permission: "warn",
  allowed: "info",
  none: "info",
};

function readCachedDay(): Day | null {
  try {
    return JSON.parse(localStorage.getItem(DAY_CACHE) ?? "null");
  } catch {
    return null;
  }
}

const hhmm = (d: Date) => d.toTimeString().slice(0, 5);

export default function Kpp() {
  const me = useMe();
  const canMark = me.role === "guard" || me.role === "admin";
  const [day, setDay] = useState<Day | null>(readCachedDay);
  const [query, setQuery] = useState("");
  const [banner, setBanner] = useState<{ text: string; kind: BannerKind } | null>(null);
  const [online, setOnline] = useState(true);
  const [pending, setPending] = useState(queued().length);
  const [busy, setBusy] = useState(false);
  const input = useRef<HTMLInputElement>(null);

  const load = useCallback(async () => {
    try {
      const d = await api<Day>("/api/day");
      setDay(d);
      setOnline(true);
      try {
        localStorage.setItem(DAY_CACHE, JSON.stringify(d));
      } catch {
        /* не критично */
      }
    } catch (e) {
      if (e instanceof OfflineError) setOnline(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);
  useLiveUpdates(load);

  // Офлайн-очередь: отправляем при появлении связи и раз в 15 секунд
  const tryFlush = useCallback(async () => {
    if (queued().length === 0) return;
    const result = await flush();
    setPending(queued().length);
    if (result.sent) {
      setOnline(true);
      load();
    }
    if (result.failed.length) setBanner({ kind: "warn", text: `Не удалось внести: ${result.failed.join("; ")}` });
  }, [load]);

  useEffect(() => {
    const timer = window.setInterval(tryFlush, 15000);
    window.addEventListener("online", tryFlush);
    tryFlush();
    return () => {
      window.clearInterval(timer);
      window.removeEventListener("online", tryFlush);
    };
  }, [tryFlush]);

  // Строки с учётом отметок, ещё не дошедших до сервера
  const rows: DayRow[] = useMemo(() => {
    const q = new Map(queued().map((item) => [item.student_id, item]));
    return (day?.rows ?? []).map((r) => {
      const item = q.get(r.student_id);
      if (!item || r.exited) return r;
      return { ...r, exited: true, exit_time: hhmm(new Date(item.client_time)), exit_offline: true, color: "green" as const };
    });
  }, [day, pending]); // pending меняется, когда очередь пополнилась или ушла на сервер

  const result = useMemo(
    () => search(query, rows.map((r) => ({ ...r, id: r.student_id }))),
    [query, rows],
  );

  const done = () => {
    setQuery("");
    setBusy(false);
    input.current?.focus();
  };

  const mark = async (row: DayRow) => {
    setBusy(true);
    try {
      const r = await api<ExitResult>("/api/exits", { method: "POST", json: { student_id: row.student_id } });
      setBanner({ text: r.message, kind: BANNER_KIND[r.status] });
      load();
    } catch (e) {
      if (e instanceof OfflineError) {
        const now = new Date();
        enqueue({ student_id: row.student_id, full_name: row.full_name, client_time: now.toISOString() });
        setPending(queued().length);
        setOnline(false);
        setBanner({ kind: "warn", text: `📴 Нет связи. ${row.full_name} — выход ${hhmm(now)} сохранён и уйдёт на сервер позже` });
      } else {
        setBanner({ kind: "warn", text: (e as ApiError).message });
        load();
      }
    }
    done();
  };

  const cancel = async (row: DayRow) => {
    if (!window.confirm(`Снять отметку выхода: ${row.full_name}?`)) return;
    setBusy(true);
    try {
      const r = await api<ExitResult>(`/api/exits/${row.student_id}/cancel`, { method: "POST" });
      setBanner({ text: r.message, kind: "info" });
      load();
    } catch (e) {
      setBanner({ kind: "warn", text: (e as Error).message });
    }
    done();
  };

  const onKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Escape") setQuery("");
    // Один найденный и ещё не вышел — Enter сразу отмечает
    if (e.key === "Enter" && canMark && !busy && result.items.length === 1 && !result.items[0].exited) {
      mark(result.items[0]);
    }
  };

  const stats = useMemo(
    () => ({
      total: rows.length,
      waiting: rows.filter((r) => r.status === "allowed").length,
      exited: rows.filter((r) => r.exited).length,
      noPermission: rows.filter((r) => r.status === "no_permission").length,
    }),
    [rows],
  );

  return (
    <>
      <TopBar title={`КПП · ${day ? formatDate(day.date) : ""}`} />
      <main className="page kpp">
        {!online && <div className="offline">📴 Нет связи с сервером. Поиск работает по последнему списку, отметки сохраняются.</div>}
        {pending > 0 && <div className="offline">Ожидают отправки: {pending}</div>}
        {day && !day.working_day && <div className="banner info">Сегодня нерабочий день по календарю школы</div>}

        <div>
          <input
            ref={input}
            className="kpp-search"
            placeholder="Фамилия или имя ученика"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={onKey}
            autoFocus
            autoComplete="off"
            autoCorrect="off"
            spellCheck={false}
            aria-label="Поиск ученика"
          />
          <div className="kpp-hint">{query ? result.hint : canMark ? "Начните вводить — список появится сразу. Enter отмечает, если найден один." : ""}</div>
        </div>

        {banner && (
          <div className={`banner ${banner.kind}`} role="status">
            {banner.text}
          </div>
        )}

        {query && result.items.length > 0 && (
          <div className="results">
            {result.items.map((r) => (
              <div key={r.student_id} className={`result c-${r.color}`}>
                <div>
                  <div className="name">{r.full_name}</div>
                  <div className="meta tnum">
                    {r.class_name}
                    {r.advisory !== r.class_name && ` · ${r.advisory}`}
                    {r.allowed_time && ` · разрешено с ${r.allowed_time}`}
                    {r.reason && ` · ${r.reason}`}
                    {r.exited && ` · вышел в ${r.exit_time}${r.exit_offline ? " (без связи)" : ""}`}
                  </div>
                </div>
                {canMark &&
                  (r.exited ? (
                    <button className="btn danger" disabled={busy} onClick={() => cancel(r)}>
                      Снять отметку
                    </button>
                  ) : (
                    <button className="btn primary" disabled={busy} onClick={() => mark(r)}>
                      Вышел
                    </button>
                  ))}
              </div>
            ))}
          </div>
        )}

        <div className="stats tnum">
          <span>
            Всего <b>{stats.total}</b>
          </span>
          <span>
            🟨 Ждут выхода <b>{stats.waiting}</b>
          </span>
          <span>
            🟩 Вышли <b>{stats.exited}</b>
          </span>
          <span>
            ⚠️ Без разрешения <b>{stats.noPermission}</b>
          </span>
        </div>

        <div className="table-wrap">
          <table className="list">
            <thead>
              <tr>
                <th>ФИО</th>
                <th>Класс</th>
                <th className="hide-sm">Эдвайзери</th>
                <th>Разрешено</th>
                <th>Вышел</th>
                <th className="hide-sm">Причина</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.student_id} className={r.color ? `c-${r.color}` : ""}>
                  <td>{r.full_name}</td>
                  <td>{r.class_name}</td>
                  <td className="hide-sm">{r.advisory}</td>
                  <td className="tnum">{r.allowed_time}</td>
                  <td className="tnum">
                    {r.exit_time}
                    {r.status === "early" && " 🟧"}
                    {r.status === "no_permission" && " ⚠️"}
                    {r.exit_offline && " 📴"}
                  </td>
                  <td className="hide-sm">{r.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </>
  );
}
