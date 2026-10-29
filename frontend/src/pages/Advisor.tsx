import { useCallback, useEffect, useState, type KeyboardEvent } from "react";
import { TopBar, useMe } from "../App";
import { api, formatDate, type AdvisorRow, type AdvisoryView } from "../lib/api";
import { useLiveUpdates } from "../lib/live";
import { webApp } from "../lib/telegram";

const LAST_TAB = "kpp-advisory";

function StudentCard({ row, editable, onSaved }: { row: AdvisorRow; editable: boolean; onSaved: (r: AdvisorRow) => void }) {
  const [time, setTime] = useState(row.time);
  const [reason, setReason] = useState(row.reason);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  // Обновление с сервера не затирает то, что эдвайзер сейчас печатает
  const [focused, setFocused] = useState(false);
  useEffect(() => {
    if (!focused) {
      setTime(row.time);
      setReason(row.reason);
    }
  }, [row.time, row.reason, focused]);

  const save = async () => {
    setFocused(false);
    if (time.trim() === row.time && reason.trim() === row.reason) return;
    setSaving(true);
    setError("");
    try {
      const saved = await api<AdvisorRow>(`/api/advisor/students/${row.student_id}/permission`, {
        method: "PUT",
        json: { time, reason },
      });
      onSaved(saved);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSaving(false);
    }
  };

  const onEnter = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") (e.target as HTMLInputElement).blur();
  };

  return (
    <div className={`student-card ${row.color ? `c-${row.color}` : ""}`}>
      <div className="top">
        <span className="name">{row.full_name}</span>
        <span className="muted">{row.class_name}</span>
      </div>
      <div className="inputs">
        <input
          className="input tnum"
          placeholder="Время"
          inputMode="text"
          value={time}
          disabled={!editable || saving}
          onFocus={() => setFocused(true)}
          onChange={(e) => setTime(e.target.value)}
          onBlur={save}
          onKeyDown={onEnter}
          aria-label={`Время выхода: ${row.full_name}`}
        />
        <input
          className="input"
          placeholder="Причина (необязательно)"
          value={reason}
          disabled={!editable || saving}
          onFocus={() => setFocused(true)}
          onChange={(e) => setReason(e.target.value)}
          onBlur={save}
          onKeyDown={onEnter}
          aria-label={`Причина: ${row.full_name}`}
        />
      </div>
      {(row.status || row.exit || saving || error) && (
        <div className="status tnum">
          {saving ? "Сохраняю…" : row.status}
          {row.exit && (
            <b>
              {" "}
              · {row.exit}
              {row.early && " 🟧 раньше времени"}
            </b>
          )}
          {error && <span className="error"> {error}</span>}
        </div>
      )}
    </div>
  );
}

export default function Advisor() {
  const me = useMe();
  const [active, setActive] = useState<number | null>(() => {
    let saved = NaN;
    try {
      saved = Number(localStorage.getItem(LAST_TAB));
    } catch {
      /* хранилище недоступно */
    }
    return me.advisories.some((a) => a.id === saved) ? saved : (me.advisories[0]?.id ?? null);
  });
  const [view, setView] = useState<AdvisoryView | null>(null);
  const [error, setError] = useState("");
  const [help, setHelp] = useState(false);

  useEffect(() => {
    const tg = webApp();
    tg?.ready();
    tg?.expand();
  }, []);

  const load = useCallback(async () => {
    if (active == null) return;
    try {
      setView(await api<AdvisoryView>(`/api/advisor/advisories/${active}`));
      setError("");
    } catch (e) {
      setError((e as Error).message);
    }
  }, [active]);

  useEffect(() => {
    setView(null);
    load();
    try {
      if (active != null) localStorage.setItem(LAST_TAB, String(active));
    } catch {
      /* не критично */
    }
  }, [active, load]);
  useLiveUpdates(load);

  const onSaved = (saved: AdvisorRow) =>
    setView((v) => v && { ...v, rows: v.rows.map((r) => (r.student_id === saved.student_id ? saved : r)) });

  // Нераспознанное время («абв») — не разрешение
  const permitted = view?.rows.filter((r) => r.status.startsWith("✅")).length ?? 0;
  const exited = view?.rows.filter((r) => r.exit).length ?? 0;

  return (
    <>
      <TopBar title={`Разовые выходы · ${formatDate(me.today)}`} />
      <main className="page">
        {me.advisories.length === 0 && <div className="card">Вам ещё не назначена эдвайзери. Обратитесь к администратору.</div>}

        {me.advisories.length > 1 && (
          <div className="tabs" role="tablist">
            {me.advisories.map((a) => (
              <button key={a.id} className={a.id === active ? "active" : ""} onClick={() => setActive(a.id)} role="tab">
                {a.name}
              </button>
            ))}
          </div>
        )}

        {view && (
          <>
            <div className="row" style={{ justifyContent: "space-between", marginBottom: 10 }}>
              <span className="muted tnum">
                {view.name}: разрешено {permitted}, вышли {exited}
              </span>
              <button className="btn small" onClick={() => setHelp(!help)}>
                {help ? "Скрыть" : "Как заполнять"}
              </button>
            </div>
            {help && (
              <div className="card" style={{ marginBottom: 10 }}>
                Впишите время, с которого ученику можно выйти сегодня: <b>15:05</b>, <b>15.05</b>, <b>1505</b> или <b>9:30</b>.
                Причина — по желанию. Разрешение сразу видно охране. Сотрите время — разрешение отменится. Когда ученик выйдет,
                появится 🚪 со временем выхода. Завтра всё начнётся с чистого листа.
              </div>
            )}
            {!view.editable && <div className="card muted">Только просмотр</div>}
            <div className="advisor-list">
              {view.rows.map((r) => (
                <StudentCard key={r.student_id} row={r} editable={view.editable} onSaved={onSaved} />
              ))}
            </div>
          </>
        )}
        {error && <div className="error">{error}</div>}
      </main>
    </>
  );
}
