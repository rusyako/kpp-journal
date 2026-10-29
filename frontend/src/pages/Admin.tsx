import { useCallback, useEffect, useMemo, useState, type FormEvent } from "react";
import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import { TopBar, useMe } from "../App";
import { api, formatDate, type Role } from "../lib/api";
import { words } from "../lib/normalize";
import { AuditView, ReportView } from "./Reports";

// ---------- Типы ----------

interface Advisory {
  id: number;
  name: string;
  kind: string;
  students: number;
  advisors: { name: string; telegram: boolean }[];
}

interface Student {
  id: number;
  full_name: string;
  class_name: string;
  advisory_id: number;
  advisory: string;
  active: boolean;
}

interface User {
  id: number;
  role: Role;
  display_name: string;
  username: string | null;
  email: string | null;
  has_password: boolean;
  telegram: boolean;
  advisory_ids: number[];
  receives_report: boolean;
  active: boolean;
}

interface ImportResult {
  applied: boolean;
  students: number;
  warnings: string[];
  diff: Record<string, string[]> & { empty: boolean };
}

const ROLE_LABEL: Record<Role, string> = {
  admin: "Администратор",
  guard: "Охрана",
  advisor: "Эдвайзер",
  viewer: "Руководство",
};

function useAdvisories() {
  const [list, setList] = useState<Advisory[]>([]);
  const load = useCallback(() => {
    api<Advisory[]>("/api/admin/advisories").then(setList).catch(() => undefined);
  }, []);
  useEffect(load, [load]);
  return { list, reload: load };
}

// ---------- Ученики и загрузка списка (Ф-22, Ф-23) ----------

const DIFF_TITLES: Record<string, string> = {
  added: "Новые",
  moved: "Переведены в другой класс",
  advisory_changed: "Сменили эдвайзери",
  reactivated: "Вернулись",
  removed: "Выбыли",
  new_advisories: "Новые эдвайзери",
  removed_advisories: "Исчезнувшие эдвайзери",
};

function ImportCard({ onApplied }: { onApplied: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<ImportResult | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const run = async (apply: boolean) => {
    if (!file) return;
    setBusy(true);
    setError("");
    const form = new FormData();
    form.append("file", file);
    form.append("apply", String(apply));
    try {
      const r = await api<ImportResult>("/api/admin/import", { method: "POST", body: form });
      setResult(r);
      if (apply) onApplied();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card" style={{ display: "grid", gap: 10 }}>
      <b>Загрузить список из Excel</b>
      <span className="muted">Файл .xlsx с листом «Для журнала»: ФИО | Класс | Эдвайзери. Сначала покажем изменения, потом примените.</span>
      <div className="row">
        <input
          type="file"
          accept=".xlsx"
          onChange={(e) => {
            setFile(e.target.files?.[0] ?? null);
            setResult(null);
          }}
        />
        <button className="btn" disabled={!file || busy} onClick={() => run(false)}>
          Показать изменения
        </button>
        {result && !result.applied && !result.diff.empty && (
          <button className="btn primary" disabled={busy} onClick={() => run(true)}>
            Применить
          </button>
        )}
      </div>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="diff">
          <div>
            {result.applied ? "✅ Применено. " : ""}Учеников в файле: {result.students}
            {result.diff.empty && " — изменений нет"}
          </div>
          {Object.entries(DIFF_TITLES).map(([key, title]) =>
            result.diff[key]?.length ? (
              <div key={key}>
                <h4>
                  {title}: {result.diff[key].length}
                </h4>
                <ul>
                  {result.diff[key].map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              </div>
            ) : null,
          )}
          {result.warnings.length > 0 && (
            <>
              <h4>⚠️ Пропущенные строки: {result.warnings.length}</h4>
              <ul>
                {result.warnings.map((w) => (
                  <li key={w}>{w}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

function StudentForm({
  student,
  advisories,
  onDone,
}: {
  student: Student | null;
  advisories: Advisory[];
  onDone: () => void;
}) {
  const [name, setName] = useState(student?.full_name ?? "");
  const [klass, setKlass] = useState(student?.class_name ?? "");
  const [advisoryId, setAdvisoryId] = useState<number | "">(student?.advisory_id ?? "");
  const [active, setActive] = useState(student?.active ?? true);
  const [error, setError] = useState("");
  const groups = advisories.filter((a) => a.kind === "group");
  const grade = parseInt(klass, 10);
  const needsGroup = grade >= 6 && grade <= 12;

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await api(student ? `/api/admin/students/${student.id}` : "/api/admin/students", {
        method: student ? "PUT" : "POST",
        json: { full_name: name, class_name: klass, advisory_id: advisoryId || null, active },
      });
      onDone();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <form className="card grid-2" onSubmit={submit}>
      <label className="field">
        <span>ФИО</span>
        <input className="input" value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <label className="field">
        <span>Класс (7A, 1B, Alpha α1, CDC)</span>
        <input className="input" value={klass} onChange={(e) => setKlass(e.target.value)} required />
      </label>
      {needsGroup && (
        <label className="field">
          <span>Эдвайзери</span>
          <select className="input" value={advisoryId} onChange={(e) => setAdvisoryId(Number(e.target.value) || "")} required>
            <option value="">— выберите —</option>
            {groups.map((a) => (
              <option key={a.id} value={a.id}>
                {a.name}
              </option>
            ))}
          </select>
        </label>
      )}
      {student && (
        <label className="row">
          <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} /> Учится в школе
        </label>
      )}
      <div className="row">
        <button className="btn primary">{student ? "Сохранить" : "Добавить"}</button>
        <button type="button" className="btn" onClick={onDone}>
          Отмена
        </button>
        {error && <span className="error">{error}</span>}
      </div>
    </form>
  );
}

function StudentsTab() {
  const [students, setStudents] = useState<Student[]>([]);
  const [filter, setFilter] = useState("");
  const [editing, setEditing] = useState<Student | "new" | null>(null);
  const advisories = useAdvisories();

  const load = useCallback(() => {
    api<Student[]>("/api/admin/students").then(setStudents).catch(() => undefined);
    advisories.reload();
  }, [advisories.reload]);
  useEffect(load, [load]);

  const shown = useMemo(() => {
    const q = words(filter);
    if (!q.length) return students;
    return students.filter((s) => {
      const hay = words(`${s.full_name} ${s.class_name} ${s.advisory}`);
      return q.every((w) => hay.some((h) => h.startsWith(w)));
    });
  }, [students, filter]);

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <ImportCard onApplied={load} />
      <div className="row">
        <input className="input" style={{ maxWidth: 320 }} placeholder="Фильтр: ФИО, класс, эдвайзери" value={filter} onChange={(e) => setFilter(e.target.value)} />
        <button className="btn" onClick={() => setEditing("new")}>
          + Ученик
        </button>
        <span className="muted tnum">
          {students.filter((s) => s.active).length} учатся · {students.filter((s) => !s.active).length} выбыли
        </span>
      </div>
      {editing && (
        <StudentForm
          key={editing === "new" ? "new" : editing.id}
          student={editing === "new" ? null : editing}
          advisories={advisories.list}
          onDone={() => {
            setEditing(null);
            load();
          }}
        />
      )}
      <div className="table-wrap">
        <table className="list">
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Класс</th>
              <th>Эдвайзери</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {shown.map((s) => (
              <tr key={s.id} className={s.active ? "" : "muted"}>
                <td>
                  {s.full_name}
                  {!s.active && " (выбыл)"}
                </td>
                <td>{s.class_name}</td>
                <td>{s.advisory}</td>
                <td>
                  <button className="btn small" onClick={() => setEditing(s)}>
                    Изменить
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ---------- Эдвайзери ----------

function AdvisoriesTab() {
  const { list } = useAdvisories();
  return (
    <div className="table-wrap">
      <table className="list">
        <thead>
          <tr>
            <th>Эдвайзери</th>
            <th>Учеников</th>
            <th>Эдвайзеры</th>
          </tr>
        </thead>
        <tbody>
          {list.map((a) => (
            <tr key={a.id}>
              <td>{a.name}</td>
              <td className="tnum">{a.students}</td>
              <td>
                {a.advisors.length === 0 ? (
                  <span className="error">не назначен</span>
                ) : (
                  a.advisors.map((u) => `${u.name}${u.telegram ? "" : " (без Telegram)"}`).join(", ")
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ---------- Пользователи и приглашения ----------

function UserForm({ user, advisories, onDone }: { user: User | null; advisories: Advisory[]; onDone: () => void }) {
  const [form, setForm] = useState({
    role: user?.role ?? ("advisor" as Role),
    display_name: user?.display_name ?? "",
    username: user?.username ?? "",
    email: user?.email ?? "",
    password: "",
    advisory_ids: user?.advisory_ids ?? [],
    receives_report: user?.receives_report ?? false,
    active: user?.active ?? true,
    unlink_telegram: false,
  });
  const [error, setError] = useState("");
  const set = <K extends keyof typeof form>(key: K, value: (typeof form)[K]) => setForm({ ...form, [key]: value });

  const toggleAdvisory = (id: number) =>
    set("advisory_ids", form.advisory_ids.includes(id) ? form.advisory_ids.filter((x) => x !== id) : [...form.advisory_ids, id]);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await api(user ? `/api/admin/users/${user.id}` : "/api/admin/users", {
        method: user ? "PUT" : "POST",
        json: { ...form, username: form.username || null, email: form.email || null, password: form.password || null },
      });
      onDone();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <form className="card" style={{ display: "grid", gap: 10 }} onSubmit={submit}>
      <div className="grid-2">
        <label className="field">
          <span>Роль</span>
          <select className="input" value={form.role} onChange={(e) => set("role", e.target.value as Role)}>
            {Object.entries(ROLE_LABEL).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <label className="field">
          <span>Имя</span>
          <input className="input" value={form.display_name} onChange={(e) => set("display_name", e.target.value)} required />
        </label>
        <label className="field">
          <span>Логин (для входа с компьютера)</span>
          <input className="input" value={form.username} onChange={(e) => set("username", e.target.value)} autoComplete="off" />
        </label>
        <label className="field">
          <span>{user?.has_password ? "Новый пароль (пусто — не менять)" : "Пароль"}</span>
          <input className="input" type="password" value={form.password} onChange={(e) => set("password", e.target.value)} autoComplete="new-password" />
        </label>
        <label className="field">
          <span>Почта (для журнала действий)</span>
          <input className="input" type="email" value={form.email} onChange={(e) => set("email", e.target.value)} />
        </label>
      </div>
      {form.role === "advisor" && (
        <div className="field">
          <span>Эдвайзери</span>
          <div className="row">
            {advisories.map((a) => (
              <label key={a.id} className="row" style={{ gap: 4 }}>
                <input type="checkbox" checked={form.advisory_ids.includes(a.id)} onChange={() => toggleAdvisory(a.id)} />
                {a.name}
              </label>
            ))}
          </div>
        </div>
      )}
      <div className="row">
        <label className="row" style={{ gap: 4 }}>
          <input type="checkbox" checked={form.receives_report} onChange={(e) => set("receives_report", e.target.checked)} />
          Получает отчёт в Telegram
        </label>
        {user && (
          <label className="row" style={{ gap: 4 }}>
            <input type="checkbox" checked={form.active} onChange={(e) => set("active", e.target.checked)} />
            Доступ включён
          </label>
        )}
        {user?.telegram && (
          <label className="row" style={{ gap: 4 }}>
            <input type="checkbox" checked={form.unlink_telegram} onChange={(e) => set("unlink_telegram", e.target.checked)} />
            Отвязать Telegram
          </label>
        )}
      </div>
      <div className="row">
        <button className="btn primary">{user ? "Сохранить" : "Создать"}</button>
        <button type="button" className="btn" onClick={onDone}>
          Отмена
        </button>
        {error && <span className="error">{error}</span>}
      </div>
    </form>
  );
}

function UsersTab() {
  const [users, setUsers] = useState<User[]>([]);
  const [editing, setEditing] = useState<User | "new" | null>(null);
  const [invite, setInvite] = useState<{ name: string; code: string; link: string | null } | null>(null);
  const advisories = useAdvisories();
  const names = useMemo(() => new Map(advisories.list.map((a) => [a.id, a.name])), [advisories.list]);

  const load = useCallback(() => {
    api<User[]>("/api/admin/users").then(setUsers).catch(() => undefined);
  }, []);
  useEffect(load, [load]);

  const makeInvite = async (u: User) => {
    const r = await api<{ code: string; link: string | null }>(`/api/admin/users/${u.id}/invite`, { method: "POST" });
    setInvite({ name: u.display_name, ...r });
  };

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <div className="row">
        <button className="btn" onClick={() => setEditing("new")}>
          + Пользователь
        </button>
        <span className="muted">Эдвайзеру и руководству отправьте приглашение — по нему Telegram привязывается к журналу.</span>
      </div>
      {editing && (
        <UserForm
          key={editing === "new" ? "new" : editing.id}
          user={editing === "new" ? null : editing}
          advisories={advisories.list}
          onDone={() => {
            setEditing(null);
            load();
            advisories.reload();
          }}
        />
      )}
      {invite && (
        <div className="card" style={{ display: "grid", gap: 6 }}>
          <b>Приглашение для: {invite.name}</b>
          {invite.link ? (
            <>
              <span>Отправьте эту ссылку человеку (действует 7 дней, одноразовая):</span>
              <code style={{ wordBreak: "break-all" }}>{invite.link}</code>
              <div className="row">
                <button className="btn small" onClick={() => navigator.clipboard?.writeText(invite.link!)}>
                  Скопировать
                </button>
                <button className="btn small" onClick={() => setInvite(null)}>
                  Закрыть
                </button>
              </div>
            </>
          ) : (
            <span>
              Бот не настроен (нет TELEGRAM_BOT_USERNAME). Код: <code>{invite.code}</code> — команда боту: /start {invite.code}
            </span>
          )}
        </div>
      )}
      <div className="table-wrap">
        <table className="list">
          <thead>
            <tr>
              <th>Имя</th>
              <th>Роль</th>
              <th>Вход</th>
              <th>Эдвайзери</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className={u.active ? "" : "muted"}>
                <td>
                  {u.display_name}
                  {!u.active && " (отключён)"}
                  {u.receives_report && " · 📊"}
                </td>
                <td>{ROLE_LABEL[u.role]}</td>
                <td>
                  {[u.username && `логин ${u.username}`, u.telegram ? "Telegram ✅" : u.role === "advisor" ? "Telegram ❌" : ""]
                    .filter(Boolean)
                    .join(" · ")}
                </td>
                <td>{u.advisory_ids.map((id) => names.get(id)).join(", ")}</td>
                <td className="row" style={{ flexWrap: "nowrap" }}>
                  <button className="btn small" onClick={() => setEditing(u)}>
                    Изменить
                  </button>
                  <button className="btn small" onClick={() => makeInvite(u)}>
                    Приглашение
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ---------- Календарь ----------

function CalendarTab() {
  const [days, setDays] = useState<{ date: string; is_working: boolean; note: string }[]>([]);
  const [date, setDate] = useState("");
  const [isWorking, setIsWorking] = useState(false);
  const [note, setNote] = useState("");

  const load = useCallback(() => {
    api<typeof days>("/api/admin/school-days").then(setDays).catch(() => undefined);
  }, []);
  useEffect(load, [load]);

  const add = async (e: FormEvent) => {
    e.preventDefault();
    await api(`/api/admin/school-days/${date}`, { method: "PUT", json: { is_working: isWorking, note } });
    setDate("");
    setNote("");
    load();
  };

  const remove = async (d: string) => {
    await api(`/api/admin/school-days/${d}`, { method: "DELETE" });
    load();
  };

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <span className="muted">По умолчанию рабочие дни — пн–сб. Здесь — каникулы, праздники и перенесённые дни. В нерабочий день отчёт не рассылается.</span>
      <form className="card row" onSubmit={add}>
        <input className="input" style={{ width: "auto" }} type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
        <select className="input" style={{ width: "auto" }} value={String(isWorking)} onChange={(e) => setIsWorking(e.target.value === "true")}>
          <option value="false">Нерабочий</option>
          <option value="true">Рабочий</option>
        </select>
        <input className="input" style={{ maxWidth: 260 }} placeholder="Комментарий (каникулы, праздник)" value={note} onChange={(e) => setNote(e.target.value)} />
        <button className="btn primary">Добавить</button>
      </form>
      <table className="list">
        <tbody>
          {days.map((d) => (
            <tr key={d.date}>
              <td className="tnum">{formatDate(d.date)}</td>
              <td>{d.is_working ? "Рабочий" : "Нерабочий"}</td>
              <td>{d.note}</td>
              <td>
                <button className="btn small danger" onClick={() => remove(d.date)}>
                  Удалить
                </button>
              </td>
            </tr>
          ))}
          {days.length === 0 && (
            <tr>
              <td className="muted">Исключений впереди нет</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

// ---------- Отчёты и журнал ----------

function ReportsTab() {
  const me = useMe();
  const [date, setDate] = useState(me.today);
  const [audit, setAudit] = useState(false);
  return (
    <div style={{ display: "grid", gap: 12 }}>
      <div className="row">
        <input className="input" style={{ width: "auto" }} type="date" value={date} max={me.today} onChange={(e) => setDate(e.target.value || me.today)} />
        <div className="tabs" style={{ margin: 0 }}>
          <button className={!audit ? "active" : ""} onClick={() => setAudit(false)}>
            Отчёт
          </button>
          <button className={audit ? "active" : ""} onClick={() => setAudit(true)}>
            Журнал действий
          </button>
        </div>
      </div>
      {audit ? <AuditView date={date} /> : <ReportView date={date} />}
    </div>
  );
}

// ---------- Проверка системы (Ф-25) ----------

function HealthTab() {
  const [checks, setChecks] = useState<{ name: string; ok: boolean; detail: string }[] | null>(null);
  const load = useCallback(() => {
    setChecks(null);
    api<typeof checks>("/api/admin/health").then(setChecks).catch(() => setChecks([]));
  }, []);
  useEffect(load, [load]);

  return (
    <div className="card" style={{ display: "grid", gap: 12 }}>
      <div className="row">
        <b>Проверка системы</b>
        <button className="btn small" onClick={load}>
          Проверить снова
        </button>
      </div>
      {!checks ? (
        <span className="muted">Проверяю…</span>
      ) : (
        <ul className="checklist">
          {checks.map((c) => (
            <li key={c.name}>
              <span>{c.ok ? "✅" : "⚠️"}</span>
              <span>
                {c.name}
                {c.detail && <div className="muted">{c.detail}</div>}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

const TABS = [
  { path: "students", label: "Ученики", el: <StudentsTab /> },
  { path: "users", label: "Пользователи", el: <UsersTab /> },
  { path: "advisories", label: "Эдвайзери", el: <AdvisoriesTab /> },
  { path: "calendar", label: "Календарь", el: <CalendarTab /> },
  { path: "reports", label: "Отчёты", el: <ReportsTab /> },
  { path: "health", label: "Проверка", el: <HealthTab /> },
];

export default function Admin() {
  return (
    <>
      <TopBar title="Управление" />
      <main className="page">
        <div className="tabs">
          {TABS.map((t) => (
            <NavLink key={t.path} to={`/admin/${t.path}`}>
              {t.label}
            </NavLink>
          ))}
        </div>
        <Routes>
          {TABS.map((t) => (
            <Route key={t.path} path={t.path} element={t.el} />
          ))}
          <Route path="*" element={<Navigate to="students" replace />} />
        </Routes>
      </main>
    </>
  );
}
