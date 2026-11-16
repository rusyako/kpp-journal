import { useState, type FormEvent } from "react";
import { api } from "../lib/api";
import PasswordInput from "../components/PasswordInput";

export const MIN_PASSWORD_LENGTH = 8;

/**
 * Смена пароля. forced — после входа с временным паролем: другого пути дальше нет.
 */
export default function ChangePassword({
  forced,
  username,
  onDone,
  onLogout,
}: {
  forced: boolean;
  username: string | null;
  onDone: () => void;
  onLogout?: () => void;
}) {
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [repeat, setRepeat] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  const tooShort = next.length > 0 && next.length < MIN_PASSWORD_LENGTH;
  const mismatch = repeat.length > 0 && next !== repeat;

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    if (next !== repeat) return setError("Пароли не совпадают");
    setBusy(true);
    setError("");
    try {
      await api("/api/auth/change-password", {
        method: "POST",
        json: { current_password: current, new_password: next },
      });
      setDone(true);
      setCurrent("");
      setNext("");
      setRepeat("");
      onDone();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="login card" onSubmit={submit}>
      <h2 style={{ margin: 0 }}>{forced ? "Придумайте свой пароль" : "Сменить пароль"}</h2>
      {forced && (
        <span className="muted">
          Вы вошли с временным паролем от администратора. Придумайте постоянный — его будете знать только вы.
        </span>
      )}
      {/* Подсказка менеджеру паролей браузера, для какого логина сохранить пароль */}
      <input type="text" name="username" autoComplete="username" value={username ?? ""} readOnly hidden />
      {/* После входа с временным паролем его не спрашиваем ещё раз — сразу новый */}
      {!forced && (
        <label className="field">
          <span>Текущий пароль</span>
          <PasswordInput
            className="input"
            autoComplete="current-password"
            value={current}
            onChange={(e) => setCurrent(e.target.value)}
            autoFocus
          />
        </label>
      )}
      <label className="field">
        <span>Новый пароль</span>
        <PasswordInput
          className="input"
          autoComplete="new-password"
          value={next}
          onChange={(e) => setNext(e.target.value)}
          autoFocus={forced}
        />
      </label>
      <label className="field">
        <span>Повторите новый пароль</span>
        <PasswordInput autoComplete="new-password" value={repeat} onChange={(e) => setRepeat(e.target.value)} />
      </label>
      <span className={tooShort ? "error" : "muted"}>
        Не короче {MIN_PASSWORD_LENGTH} символов, без логина и не из простых вроде «Qwerty123!».
        Удобно взять фразу из нескольких слов.
      </span>
      {mismatch && <div className="error">Пароли не совпадают</div>}
      {error && <div className="error">{error}</div>}
      {done && !forced && <div className="banner ok">Пароль изменён. На других устройствах нужно войти заново.</div>}
      <button className="btn primary" disabled={busy || (!forced && !current) || next.length < MIN_PASSWORD_LENGTH || next !== repeat}>
        {busy ? "Сохраняю…" : "Сохранить пароль"}
      </button>
      {onLogout && (
        <button type="button" className="btn" onClick={onLogout}>
          Выйти
        </button>
      )}
    </form>
  );
}
