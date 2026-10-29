import { useEffect, useState } from "react";
import { TopBar, useMe } from "../App";
import { api, formatDate } from "../lib/api";

interface AuditEntry {
  time: string;
  user: string;
  student: string;
  action: string;
}

export function ReportView({ date }: { date: string }) {
  const me = useMe();
  const [sending, setSending] = useState(false);
  const [result, setResult] = useState("");
  const [nonce, setNonce] = useState(0);

  const send = async () => {
    setSending(true);
    try {
      const r = await api<{ telegram: number; email: boolean }>(`/api/admin/reports/${date}/send`, { method: "POST" });
      setResult(`Отправлено: Telegram — ${r.telegram}, почта — ${r.email ? "да" : "нет"}`);
    } catch (e) {
      setResult((e as Error).message);
    } finally {
      setSending(false);
    }
  };

  return (
    <div style={{ display: "grid", gap: 10 }}>
      <div className="row">
        <button className="btn small" onClick={() => setNonce(nonce + 1)}>
          Обновить
        </button>
        <a className="btn small" href={`/api/reports/${date}/html`} target="_blank" rel="noreferrer">
          Открыть для печати
        </a>
        {me.role === "admin" && (
          <button className="btn small" onClick={send} disabled={sending}>
            Разослать сейчас
          </button>
        )}
        <span className="muted">{result}</span>
      </div>
      <iframe key={`${date}-${nonce}`} className="report" title={`Отчёт за ${formatDate(date)}`} src={`/api/reports/${date}/html`} />
    </div>
  );
}

export function AuditView({ date }: { date: string }) {
  const [entries, setEntries] = useState<AuditEntry[] | null>(null);
  useEffect(() => {
    setEntries(null);
    api<AuditEntry[]>(`/api/audit?d=${date}`).then(setEntries).catch(() => setEntries([]));
  }, [date]);

  if (!entries) return <div className="muted">Загрузка…</div>;
  if (entries.length === 0) return <div className="muted">Записей нет</div>;
  return (
    <div className="table-wrap">
      <table className="list">
        <thead>
          <tr>
            <th>Время</th>
            <th>Кто</th>
            <th>Действие</th>
            <th>Ученик</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((e, i) => (
            <tr key={i}>
              <td className="tnum">{e.time}</td>
              <td>{e.user}</td>
              <td>{e.action}</td>
              <td>{e.student}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function Reports() {
  const me = useMe();
  const [date, setDate] = useState(me.today);
  const [tab, setTab] = useState<"report" | "audit">("report");

  return (
    <>
      <TopBar title="Отчёты" />
      <main className="page" style={{ display: "grid", gap: 12 }}>
        <div className="row">
          <input className="input" style={{ width: "auto" }} type="date" value={date} max={me.today} onChange={(e) => setDate(e.target.value || me.today)} />
          <div className="tabs" style={{ margin: 0 }}>
            <button className={tab === "report" ? "active" : ""} onClick={() => setTab("report")}>
              Отчёт за день
            </button>
            <button className={tab === "audit" ? "active" : ""} onClick={() => setTab("audit")}>
              Журнал действий
            </button>
          </div>
        </div>
        {tab === "report" ? <ReportView date={date} /> : <AuditView date={date} />}
      </main>
    </>
  );
}
