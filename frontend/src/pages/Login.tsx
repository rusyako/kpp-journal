import { useState, type FormEvent } from "react";
import { api } from "../lib/api";

export default function Login({ onLogin }: { onLogin: () => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await api("/api/auth/login", { method: "POST", json: { username, password } });
      onLogin();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="login card" onSubmit={submit}>
      <h2 style={{ margin: 0 }}>Журнал КПП</h2>
      <label className="field">
        <span>Логин</span>
        <input className="input" autoComplete="username" value={username} onChange={(e) => setUsername(e.target.value)} autoFocus />
      </label>
      <label className="field">
        <span>Пароль</span>
        <input
          className="input"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      {error && <div className="error">{error}</div>}
      <button className="btn primary" disabled={busy || !username || !password}>
        Войти
      </button>
      <section className="demo-logins" aria-labelledby="demo-logins-title">
        <h3 id="demo-logins-title">Тестовые кабинеты</h3>
        <div className="muted">Выберите кабинет, чтобы заполнить данные для входа.</div>
        {[
          ["admin", "Администратор"],
          ["kpp", "Охрана КПП"],
          ["kotiki", "Куратор: Котики"],
          ["primary", "Куратор: 1A"],
          ["director", "Руководство"],
        ].map(([login, label]) => (
          <button
            key={login}
            type="button"
            className="btn demo-login"
            disabled={busy}
            onClick={() => {
              setUsername(login);
              setPassword("demo-pass-123");
              setError("");
            }}
          >
            <span>{label}</span>
            <code>{login}</code>
          </button>
        ))}
        <div>Пароль для всех: <code>demo-pass-123</code></div>
        <small className="muted">Только для тестового стенда с загруженными демо-данными. Не используйте эти аккаунты для реальных данных.</small>
      </section>
    </form>
  );
}
