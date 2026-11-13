import { useCallback, useEffect, useState, type FormEvent } from "react";
import { TopBar, useMe } from "../App";
import { api, formatDate, type AdvisorRow, type AdvisoryView } from "../lib/api";
import { useLiveUpdates } from "../lib/live";
import { webApp } from "../lib/telegram";

const LAST_TAB = "kpp-advisory";
const REASONS = ["Визит к врачу", "Поедет в визовый центр", "Дополнительные секции", "По состоянию здоровья"];

const reasonOption = (reason: string) => REASONS.includes(reason) ? reason : reason ? "other" : "";

function StudentCard({ row, editable, onSaved }: { row: AdvisorRow; editable: boolean; onSaved: (r: AdvisorRow) => void }) {
  const [time, setTime] = useState(row.time);
  const [reason, setReason] = useState(row.reason);
  const [selectedReason, setSelectedReason] = useState(() => reasonOption(row.reason));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  // Живые обновления не должны затирать несохранённый черновик.
  const [dirty, setDirty] = useState(false);
  useEffect(() => {
    if (!dirty && !saving) {
      setTime(row.time);
      setReason(row.reason);
      setSelectedReason(reasonOption(row.reason));
    }
  }, [row.time, row.reason, dirty, saving]);

  const save = async (e: FormEvent) => {
    e.preventDefault();
    if (!editable || saving || !dirty) return;
    setSaving(true);
    setError("");
    try {
      const saved = await api<AdvisorRow>(`/api/advisor/students/${row.student_id}/permission`, {
        method: "PUT",
        json: { time, reason },
      });
      onSaved(saved);
      setTime(saved.time);
      setReason(saved.reason);
      setSelectedReason(reasonOption(saved.reason));
      setDirty(false);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className={`student-card ${row.color ? `c-${row.color}` : ""}`} onSubmit={save}>
      <div className="top">
        <span className="name">{row.full_name}</span>
        <span className="muted">{row.class_name}</span>
      </div>
      <div className="inputs">
        <label className="field">
          <span>Можно выйти с</span>
          <input
            className="input tnum"
            type="time"
            step={60}
            value={time}
            disabled={!editable || saving}
            onChange={(e) => { setTime(e.target.value); setDirty(true); }}
            aria-label={`Время выхода: ${row.full_name}`}
          />
        </label>
        <label className="field">
          <span>Причина выхода</span>
          <select
            className="input"
            value={selectedReason}
            disabled={!editable || saving}
            onChange={(e) => {
              setSelectedReason(e.target.value);
              setReason(e.target.value === "other" ? "" : e.target.value);
              setDirty(true);
            }}
            aria-label={`Причина: ${row.full_name}`}
          >
            <option value="">Без причины</option>
            {REASONS.map((item) => <option key={item} value={item}>{item}</option>)}
            <option value="other">Иное (указать)</option>
          </select>
        </label>
      </div>
      {selectedReason === "other" && (
        <label className="field">
          <span>Укажите причину</span>
          <textarea
            className="input"
            rows={2}
            maxLength={500}
            required
            value={reason}
            disabled={!editable || saving}
            onChange={(e) => { setReason(e.target.value); setDirty(true); }}
            aria-label={`Другая причина: ${row.full_name}`}
            placeholder="Напишите причину выхода"
          />
        </label>
      )}
      {editable && (
        <div className="row permission-actions">
          <button className="btn primary" disabled={!dirty || saving || (selectedReason === "other" && !reason.trim())}>
            {saving ? "Сохранение..." : "Сохранить"}
          </button>
          {time && (
            <button type="button" className="btn" disabled={saving} onClick={() => { setTime(""); setDirty(true); }}>
              Убрать время
            </button>
          )}
          {dirty && <span className="muted">Изменения ещё не сохранены</span>}
        </div>
      )}
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
    </form>
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
                Нажмите на время и выберите часы и минуты, с которых ученику можно выйти сегодня.
                Выберите причину из списка или «Иное», чтобы написать свою. Нажмите «Сохранить» — разрешение увидит охрана.
                Для отмены нажмите «Убрать время», затем «Сохранить». Когда ученик выйдет,
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
