import { useCallback, useEffect, useState, type FormEvent } from "react";
import { TopBar } from "../App";
import { api } from "../lib/api";

// Экран пилота Hikvision. Кнопки «открыть турникет» здесь нет и быть не должно:
// открыть проход может только ответ success на конкретный запрос терминала.

interface Settings {
  mode: "SIMULATION" | "READ_ONLY" | "PILOT";
  control_enabled: boolean;
  control_devices: string[];
  pilot_employee_nos: string[];
  decision_budget_ms: number;
  max_event_age_s: number;
  passage_window_s: number;
}

interface Device {
  key: string;
  name: string;
  direction: "exit" | "entry";
  simulated: boolean;
  host: string;
  response_mode: string;
  active: boolean;
  control_allowed: boolean;
  model: string | null;
  firmware: string | null;
  last_event_at: string | null;
  last_health_at: string | null;
  last_health_ok: boolean | null;
  last_error: string | null;
  remote_check: { verdict: string; verdict_text: string; checked_at: string; stops: string[]; changes: { field: string; current: unknown; target: unknown }[] } | null;
}

interface Permission {
  id: number;
  employee_no: string | null;
  valid_from: string;
  valid_until: string;
  single_use: boolean;
  note: string;
  status: "active" | "pending" | "expired" | "revoked" | "used";
  used_at: string | null;
  used_by_decision_id: number | null;
}

interface Person {
  employee_no: string;
  label: string;
  active: boolean;
  terminal_user_type: string | null;
  terminal_checked_at: string | null;
  terminal_device_key: string | null;
  permissions: Permission[];
}

interface EventRow {
  id: number;
  received_at: string;
  device_key: string;
  serial_no: number | null;
  event_time: string;
  major: number | null;
  minor: number | null;
  employee_no: string | null;
  user_type: string | null;
  remote_check: boolean;
  category: string;
  duplicate_of_id: number | null;
}

interface DecisionRow {
  id: number;
  decided_at: string;
  event_id: number;
  device_key: string | null;
  employee_no: string | null;
  result: "ALLOW" | "DENY";
  user_type: string | null;
  serial_no: number | null;
  reason: string;
  detail: string;
  mode: string;
  latency_ms: number;
  command: { status: string; check_result: string } | null;
  passage: { outcome: string; source: string; exit_id: number | null } | null;
}

interface CommandRow {
  id: number;
  created_at: string;
  device_key: string | null;
  kind: string;
  method: string;
  path: string;
  check_result: string | null;
  status: string;
  http_status: number | null;
  error: string | null;
  latency_ms: number;
  decision_id: number | null;
}

interface Status {
  isolation_alerts: { decision_id: number; decided_at: string; device_key: string | null; employee_no: string | null }[];
  settings: Settings;
  pilot_enabled: boolean;
  now: string;
  devices: Device[];
  persons: Person[];
  permissions: Permission[];
  events: EventRow[];
  decisions: DecisionRow[];
  commands: CommandRow[];
}

interface SimResult {
  serial_no: number;
  door_opened: boolean;
  local: boolean;
  user_type: string | null;
  terminal: string;
  decision_id: number | null;
  trace: string[];
}

const PERM_STATUS: Record<Permission["status"], string> = {
  active: "действует",
  pending: "ещё не началось",
  expired: "истекло",
  revoked: "отменено",
  used: "использовано",
};

const CATEGORY: Record<string, string> = {
  remote_check: "запрос проверки",
  passage: "проход",
  passage_timeout: "не прошёл (таймаут)",
  reverse_passage: "обратный проход",
  door: "дверь",
  auth_ok: "опознан",
  auth_failed: "отказ опознания",
  remote_check_result: "итог проверки",
  heartbeat: "heartbeat",
  other: "другое",
};

const PASSAGE: Record<string, string> = {
  passed: "прошёл",
  timed_out: "не прошёл (таймаут)",
  reverse: "обратный проход",
  not_passed: "не прошёл",
};

const COMMAND_STATUS: Record<string, string> = {
  sent: "отправлено",
  simulated: "симуляция",
  blocked: "заблокировано режимом",
  error: "ошибка",
  timeout: "таймаут",
};

const time = (iso: string | null) => (iso ? iso.slice(11, 19) : "—");
const dateTime = (iso: string | null) => (iso ? `${iso.slice(8, 10)}.${iso.slice(5, 7)} ${iso.slice(11, 16)}` : "—");

/** "YYYY-MM-DDTHH:mm" для <input type="datetime-local"> через n минут от сейчас */
function localInput(minutes: number): string {
  const d = new Date(Date.now() + minutes * 60000);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
}

function ModeBanner({ s, enabled }: { s: Settings; enabled: boolean }) {
  const text =
    s.mode === "SIMULATION"
      ? "SIMULATION — только виртуальные терминалы, к реальному оборудованию запросов нет."
      : s.mode === "READ_ONLY"
        ? "READ_ONLY — с реальных терминалов только чтение; ответы «success» не отправляются (решения теневые)."
        : `PILOT — «success» может уйти только на: ${s.control_devices.join(", ") || "—"} (управление ${s.control_enabled ? "включено" : "выключено"}).`;
  return (
    <div className={`banner ${s.mode === "PILOT" ? "warn" : "info"}`}>
      <b>Режим {s.mode}.</b> {text} Пилот {enabled ? "включён" : "выключен — все запросы получают DENY"}.
    </div>
  );
}

function Devices({ devices, onChanged }: { devices: Device[]; onChanged: () => void }) {
  const [busy, setBusy] = useState("");
  const [msg, setMsg] = useState("");
  const check = async (key: string) => {
    setBusy(key);
    try {
      const r = await api<{ ok: boolean; error: string | null; info: Record<string, string> }>(
        `/api/pilot/devices/${key}/check`,
        { method: "POST" },
      );
      setMsg(r.ok ? `${key}: ${r.info.model} ${r.info.firmwareVersion}` : `${key}: ${r.error}`);
      onChanged();
    } catch (e) {
      setMsg((e as Error).message);
    } finally {
      setBusy("");
    }
  };
  const refresh = async (key: string) => {
    setBusy(key);
    try {
      const r = await api<{ user_type: string; numOfFace: number; numOfCard: number; verdict: string; verdict_text: string }>(
        `/api/pilot/devices/${key}/refresh`,
        { method: "POST" },
      );
      setMsg(`${key}: userType=${r.user_type}, лиц ${r.numOfFace}, карт ${r.numOfCard} · ${r.verdict}: ${r.verdict_text}`);
      onChanged();
    } catch (e) {
      setMsg((e as Error).message);
    } finally {
      setBusy("");
    }
  };
  return (
    <div className="card">
      <h3 className="pilot-h">Терминалы</h3>
      <p className="muted small">Обе кнопки только читают. Реальный терминал — только в режиме READ_ONLY/PILOT.</p>
      <div className="table-wrap">
        <table className="list">
          <thead>
            <tr>
              <th>Терминал</th>
              <th>Направление</th>
              <th>Ответ success</th>
              <th>Связь (deviceInfo)</th>
              <th>Remote Verification (visitor-only)</th>
              <th>Последнее событие</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {devices.map((d) => (
              <tr key={d.key}>
                <td>
                  <b>{d.key}</b> {d.simulated && <span className="tag">симулятор</span>}
                  <div className="muted small">{d.simulated ? d.name : `${d.host} · ${d.response_mode}`}</div>
                </td>
                <td>{d.direction === "exit" ? "выход" : "вход"}</td>
                <td>{d.control_allowed ? <span className="tag ok">разрешён</span> : <span className="tag">нет</span>}</td>
                <td>
                  {d.last_health_ok === null ? (
                    <span className="muted">не проверялась</span>
                  ) : d.last_health_ok ? (
                    <span className="tag ok">OK {time(d.last_health_at)}</span>
                  ) : (
                    <span className="tag deny" title={d.last_error ?? ""}>
                      нет · {d.last_error}
                    </span>
                  )}
                </td>
                <td>
                  {!d.remote_check ? (
                    <span className="muted">не читалось</span>
                  ) : (
                    <span title={d.remote_check.verdict_text}>
                      <span className={`tag ${d.remote_check.verdict === "STOP" ? "deny" : "ok"}`}>{d.remote_check.verdict}</span>
                      {d.remote_check.stops.length > 0 && <div className="muted small">стоп: {d.remote_check.stops.join("; ")}</div>}
                    </span>
                  )}
                </td>
                <td className="tnum">{dateTime(d.last_event_at)}</td>
                <td>
                  <div className="row">
                    <button className="btn small" disabled={busy === d.key} onClick={() => check(d.key)}>
                      Проверить связь
                    </button>
                    <button className="btn small" disabled={busy === d.key} onClick={() => refresh(d.key)}>
                      Прочитать userType и AcsCfg
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {msg && <p className="muted small">{msg}</p>}
    </div>
  );
}

function PermissionCard({ status, onChanged }: { status: Status; onChanged: () => void }) {
  const person = status.persons[0];
  const [from, setFrom] = useState(localInput(0));
  const [until, setUntil] = useState(localInput(30));
  const [singleUse, setSingleUse] = useState(true);
  const [note, setNote] = useState("");
  const [error, setError] = useState("");

  if (!person) {
    return (
      <div className="card">
        <h3 className="pilot-h">Тестовое разрешение</h3>
        <p className="muted">Запись пилота не создана — нажмите «Подготовить пилот».</p>
      </div>
    );
  }

  const create = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await api("/api/pilot/permissions", {
        method: "POST",
        json: { employee_no: person.employee_no, valid_from: from, valid_until: until, single_use: singleUse, note },
      });
      setNote("");
      onChanged();
    } catch (err) {
      setError((err as Error).message);
    }
  };
  const revoke = async (id: number) => {
    await api(`/api/pilot/permissions/${id}/revoke`, { method: "POST" }).catch((e) => setError(e.message));
    onChanged();
  };
  const current = person.permissions;

  return (
    <div className="card">
      <h3 className="pilot-h">Тестовое разрешение (PILOT, не согласие родителей)</h3>
      <p>
        employeeNo <b className="tnum">{person.employee_no}</b> · {person.label}
        <br />
        userType на терминале:{" "}
        {person.terminal_user_type ? (
          <>
            <span className={`tag ${person.terminal_user_type === "visitor" ? "ok" : ""}`}>{person.terminal_user_type}</span>{" "}
            <span className="muted small">
              ({person.terminal_device_key}, {dateTime(person.terminal_checked_at)})
            </span>
          </>
        ) : (
          <span className="muted">не прочитан</span>
        )}
      </p>
      {person.terminal_user_type === "normal" && (
        <div className="banner info">normal: терминал пускает по своим правам, kpp-journal не спрашивает.</div>
      )}
      {current.length === 0 ? (
        <div className="banner warn">Действующего или ожидающего разрешения нет → терминал получит DENY.</div>
      ) : (
        current.map((p) => (
          <div key={p.id} className={`banner ${p.status === "active" ? "ok" : "info"}`}>
            №{p.id}: {PERM_STATUS[p.status]} · {dateTime(p.valid_from)} — {dateTime(p.valid_until)} ·{" "}
            {p.single_use ? "одноразовое" : "многоразовое"} {p.note && `· ${p.note}`}{" "}
            <button className="btn small danger" onClick={() => revoke(p.id)}>
              Отменить
            </button>
          </div>
        ))
      )}
      <form className="pilot-form" onSubmit={create}>
        <label className="field">
          <span>С (время школы)</span>
          <input className="input" type="datetime-local" value={from} onChange={(e) => setFrom(e.target.value)} />
        </label>
        <label className="field">
          <span>До</span>
          <input className="input" type="datetime-local" value={until} onChange={(e) => setUntil(e.target.value)} />
        </label>
        <label className="field">
          <span>Примечание</span>
          <input className="input" value={note} maxLength={500} onChange={(e) => setNote(e.target.value)} />
        </label>
        <label className="row">
          <input type="checkbox" checked={singleUse} onChange={(e) => setSingleUse(e.target.checked)} /> одноразовое
        </label>
        <button className="btn primary">Создать разрешение</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

interface UserTypeResult {
  mode: string;
  ok: boolean;
  applied: boolean;
  from_type: string | null;
  target: string;
  request: { method: string; path: string; body: unknown } | null;
  confirm: string | null;
  problems: string[];
  steps: string[];
}

function UserTypeCard({ status, onChanged }: { status: Status; onChanged: () => void }) {
  const [to, setTo] = useState<"visitor" | "normal">("visitor");
  const [confirm, setConfirm] = useState("");
  const [result, setResult] = useState<UserTypeResult | null>(null);
  const [error, setError] = useState("");
  if (status.settings.mode !== "SIMULATION") {
    return (
      <div className="card">
        <h3 className="pilot-h">Смена userType</h3>
        <p className="muted">
          Из браузера — только на виртуальном терминале (SIMULATION). Реальный терминал: CLI <code>user_type</code> с подтверждением
          (VISITOR_REMOTE_VERIFICATION_PLAN.md).
        </p>
      </div>
    );
  }
  const run = async (apply: boolean) => {
    setError("");
    try {
      const r = await api<UserTypeResult>("/api/pilot/simulate/user-type", {
        method: "POST",
        json: { device_key: "sim-exit", to, apply, confirm: apply ? confirm : null },
      });
      setResult(r);
      if (apply) setConfirm("");
      onChanged();
    } catch (e) {
      setError((e as Error).message);
    }
  };
  return (
    <div className="card">
      <h3 className="pilot-h">Смена userType (виртуальный sim-exit)</h3>
      <div className="row">
        <select className="input" style={{ width: "auto" }} value={to} onChange={(e) => setTo(e.target.value as "visitor" | "normal")}>
          <option value="visitor">→ visitor</option>
          <option value="normal">→ normal (откат)</option>
        </select>
        <button className="btn" onClick={() => run(false)}>
          DRY_RUN
        </button>
      </div>
      {result && (
        <div style={{ marginTop: 8 }}>
          <div className={`banner ${result.ok ? (result.applied ? "ok" : "info") : "warn"}`}>
            {result.mode}: {result.ok ? "OK" : "СТОП"} {result.from_type && `· было ${result.from_type}`}
          </div>
          {result.request && <pre className="small">{JSON.stringify(result.request.body)}</pre>}
          <ol className="trace">
            {result.steps.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ol>
          {result.problems.length > 0 && <p className="error">{result.problems.join("; ")}</p>}
          {result.mode === "DRY_RUN" && result.confirm && (
            <div className="row">
              <input className="input" style={{ maxWidth: 260 }} placeholder={result.confirm} value={confirm} onChange={(e) => setConfirm(e.target.value)} />
              <button className="btn primary" disabled={confirm !== result.confirm} onClick={() => run(true)}>
                Применить
              </button>
              <span className="muted small">введите «{result.confirm}»</span>
            </div>
          )}
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

const SCENARIOS: { id: string; label: string }[] = [
  { id: "face", label: "Лицо опознано" },
  { id: "repeat_last", label: "Повтор последнего события" },
  { id: "stale", label: "Устаревшее событие" },
  { id: "card", label: "Карта вместо лица" },
  { id: "server_down", label: "kpp-journal недоступен" },
];

function Simulator({ status, onChanged }: { status: Status; onChanged: () => void }) {
  const devices = status.devices.filter((d) => d.simulated);
  const [device, setDevice] = useState("sim-exit");
  const [employeeNo, setEmployeeNo] = useState(status.settings.pilot_employee_nos[0] ?? "");
  const [result, setResult] = useState<SimResult | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (status.settings.mode !== "SIMULATION") {
    return (
      <div className="card">
        <h3 className="pilot-h">Симулятор терминала</h3>
        <p className="muted">Доступен только в режиме SIMULATION.</p>
      </div>
    );
  }

  const run = async (scenario: string) => {
    setBusy(true);
    setError("");
    try {
      setResult(await api<SimResult>("/api/pilot/simulate", { method: "POST", json: { device_key: device, employee_no: employeeNo, scenario } }));
      onChanged();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };
  const passage = async (outcome: string) => {
    if (!result?.decision_id) return;
    try {
      await api("/api/pilot/simulate/passage", { method: "POST", json: { decision_id: result.decision_id, outcome } });
      onChanged();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <div className="card">
      <h3 className="pilot-h">Симулятор терминала</h3>
      <div className="pilot-form">
        <label className="field">
          <span>Терминал</span>
          <select className="input" value={device} onChange={(e) => setDevice(e.target.value)}>
            {devices.map((d) => (
              <option key={d.key} value={d.key}>
                {d.key} ({d.direction === "exit" ? "выход" : "вход"})
              </option>
            ))}
            <option value="unknown-terminal">unknown-terminal (не зарегистрирован)</option>
          </select>
        </label>
        <label className="field">
          <span>employeeNo</span>
          <input className="input tnum" list="sim-employees" value={employeeNo} maxLength={32} onChange={(e) => setEmployeeNo(e.target.value)} />
          <datalist id="sim-employees">
            {status.settings.pilot_employee_nos.map((n) => (
              <option key={n} value={n}>
                тестовая запись
              </option>
            ))}
            <option value="1000000001">сотрудник normal</option>
            <option value="0000000001">не зарегистрирован</option>
          </datalist>
        </label>
      </div>
      <div className="row" style={{ marginTop: 8 }}>
        {SCENARIOS.map((s) => (
          <button key={s.id} className={`btn small ${s.id === "face" ? "primary" : ""}`} disabled={busy} onClick={() => run(s.id)}>
            {s.label}
          </button>
        ))}
      </div>
      {error && <p className="error">{error}</p>}
      {result && (
        <div style={{ marginTop: 10 }}>
          <div className={`banner ${result.door_opened ? "ok" : "warn"}`}>
            {result.door_opened ? "🟢 Турникет открылся (симуляция)" : "🔴 Проход закрыт"}
            {result.local ? " — локальные права терминала, без kpp-journal" : ""} · serialNo {result.serial_no}
            {result.user_type && ` · userType ${result.user_type}`}
          </div>
          <ol className="trace">
            {result.trace.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ol>
          {result.door_opened && result.decision_id && (
            <div className="row">
              <span className="muted">Что сделал человек:</span>
              <button className="btn small" onClick={() => passage("passed")}>
                Прошёл (Passing Event 0xda)
              </button>
              <button className="btn small" onClick={() => passage("timed_out")}>
                Не прошёл (0x89)
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function Decisions({ rows, onChanged }: { rows: DecisionRow[]; onChanged: () => void }) {
  const [error, setError] = useState("");
  const confirm = async (id: number, passed: boolean) => {
    setError("");
    try {
      await api(`/api/pilot/decisions/${id}/confirm`, { method: "POST", json: { passed } });
      onChanged();
    } catch (e) {
      setError((e as Error).message);
    }
  };
  return (
    <div className="card">
      <h3 className="pilot-h">Решения kpp-journal</h3>
      <p className="muted small">Решение, ответ терминалу и фактический проход — разные записи. ALLOW ещё не значит «вышел».</p>
      {error && <p className="error">{error}</p>}
      <div className="table-wrap">
        <table className="list">
          <thead>
            <tr>
              <th>№</th>
              <th>Время</th>
              <th>Терминал</th>
              <th>employeeNo</th>
              <th>userType</th>
              <th>serialNo</th>
              <th>Решение</th>
              <th>Причина</th>
              <th>Ответ терминалу</th>
              <th>Проход</th>
              <th>мс</th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 && (
              <tr>
                <td colSpan={11} className="muted">
                  Решений ещё нет
                </td>
              </tr>
            )}
            {rows.map((d) => (
              <tr key={d.id}>
                <td className="tnum">{d.id}</td>
                <td className="tnum">{time(d.decided_at)}</td>
                <td>{d.device_key ?? "?"}</td>
                <td className="tnum">{d.employee_no ?? "—"}</td>
                <td>{d.user_type ?? "—"}</td>
                <td className="tnum">{d.serial_no ?? "—"}</td>
                <td>
                  <span className={`tag ${d.result === "ALLOW" ? "ok" : "deny"}`}>{d.result}</span>
                </td>
                <td>
                  {d.detail} <span className="muted small">({d.reason})</span>
                </td>
                <td>
                  {d.command ? (
                    <>
                      {d.command.check_result} · <span className="muted">{COMMAND_STATUS[d.command.status] ?? d.command.status}</span>
                    </>
                  ) : (
                    "—"
                  )}
                </td>
                <td>
                  {d.passage ? (
                    `${PASSAGE[d.passage.outcome] ?? d.passage.outcome} (${d.passage.source === "manual" ? "вручную" : "событие"})`
                  ) : d.result === "ALLOW" && d.command?.check_result === "success" ? (
                    <span className="row">
                      <span className="muted">не подтверждён</span>
                      <button className="btn small" onClick={() => confirm(d.id, true)}>
                        Прошёл
                      </button>
                      <button className="btn small" onClick={() => confirm(d.id, false)}>
                        Не прошёл
                      </button>
                    </span>
                  ) : (
                    "—"
                  )}
                </td>
                <td className="tnum">{d.latency_ms}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Events({ rows }: { rows: EventRow[] }) {
  return (
    <div className="card">
      <h3 className="pilot-h">События терминалов</h3>
      <div className="table-wrap">
        <table className="list">
          <thead>
            <tr>
              <th>№</th>
              <th>Получено</th>
              <th>Терминал</th>
              <th>serialNo</th>
              <th>major/minor</th>
              <th>employeeNo</th>
              <th>userType</th>
              <th>Тип</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((e) => (
              <tr key={e.id}>
                <td className="tnum">{e.id}</td>
                <td className="tnum">{time(e.received_at)}</td>
                <td>{e.device_key}</td>
                <td className="tnum">{e.serial_no ?? "—"}</td>
                <td className="tnum">
                  {e.major ?? "?"}/{e.minor ?? "?"}
                </td>
                <td className="tnum">{e.employee_no ?? "—"}</td>
                <td>{e.user_type ?? "—"}</td>
                <td>
                  {CATEGORY[e.category] ?? e.category}
                  {e.duplicate_of_id && <span className="tag deny">повтор №{e.duplicate_of_id}</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Commands({ rows }: { rows: CommandRow[] }) {
  return (
    <div className="card">
      <h3 className="pilot-h">Ответы и запросы к терминалам</h3>
      <div className="table-wrap">
        <table className="list">
          <thead>
            <tr>
              <th>Время</th>
              <th>Терминал</th>
              <th>Что</th>
              <th>checkResult</th>
              <th>Статус</th>
              <th>Ошибка</th>
              <th>мс</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((c) => (
              <tr key={c.id}>
                <td className="tnum">{time(c.created_at)}</td>
                <td>{c.device_key ?? "—"}</td>
                <td>
                  {c.kind}
                  {c.path && <div className="muted small">{c.path}</div>}
                </td>
                <td>{c.check_result ?? "—"}</td>
                <td>{COMMAND_STATUS[c.status] ?? c.status}</td>
                <td className="error small">{c.error}</td>
                <td className="tnum">{c.latency_ms}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function Pilot() {
  const [status, setStatus] = useState<Status | null>(null);
  const [error, setError] = useState("");

  const load = useCallback(() => {
    api<Status>("/api/pilot/status")
      .then((s) => {
        setStatus(s);
        setError("");
      })
      .catch((e) => setError((e as Error).message));
  }, []);

  useEffect(() => {
    load();
    const t = setInterval(load, 3000);
    return () => clearInterval(t);
  }, [load]);

  const setup = async () => {
    await api("/api/pilot/setup", { method: "POST" }).catch((e) => setError(e.message));
    load();
  };
  const toggle = async () => {
    if (!status) return;
    await api("/api/pilot/enabled", { method: "POST", json: { enabled: !status.pilot_enabled } }).catch((e) => setError(e.message));
    load();
  };

  return (
    <>
      <TopBar title="Пилот Hikvision" />
      <div className="page pilot">
        {error && <div className="banner warn">{error}</div>}
        {!status ? (
          <div className="muted">Загрузка…</div>
        ) : (
          <>
            <ModeBanner s={status.settings} enabled={status.pilot_enabled} />
            {status.isolation_alerts.length > 0 && (
              <div className="banner warn">
                ⚠ Нарушение изоляции: на удалённую проверку пришёл не-visitor (решения №
                {status.isolation_alerts.map((a) => a.decision_id).join(", ")}). Фильтр remoteCheckUserTypeList не работает —
                остановить пилот и откатить настройки терминала (VISITOR_ROLLBACK.md).
              </div>
            )}
            <div className="row">
              <button className="btn" onClick={setup}>
                Подготовить пилот
              </button>
              <button className={`btn ${status.pilot_enabled ? "danger" : "primary"}`} onClick={toggle}>
                {status.pilot_enabled ? "Выключить пилот" : "Включить пилот"}
              </button>
              <span className="muted small">
                Тестовые employeeNo: {status.settings.pilot_employee_nos.join(", ")} · бюджет решения {status.settings.decision_budget_ms} мс
              </span>
            </div>
            <div className="grid-2">
              <PermissionCard status={status} onChanged={load} />
              <UserTypeCard status={status} onChanged={load} />
              <Simulator status={status} onChanged={load} />
            </div>
            <Devices devices={status.devices} onChanged={load} />
            <Decisions rows={status.decisions} onChanged={load} />
            <Events rows={status.events} />
            <Commands rows={status.commands} />
          </>
        )}
      </div>
    </>
  );
}
