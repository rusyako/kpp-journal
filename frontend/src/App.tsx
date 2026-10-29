import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { Navigate, NavLink, Route, Routes, useNavigate } from "react-router-dom";
import { api, ApiError, type Me, type Role } from "./lib/api";
import { webApp } from "./lib/telegram";
import Admin from "./pages/Admin";
import Advisor from "./pages/Advisor";
import Kpp from "./pages/Kpp";
import Login from "./pages/Login";
import Reports from "./pages/Reports";

const ME_CACHE = "kpp-me";

interface Session {
  me: Me;
  reload: () => void;
}

const SessionContext = createContext<Session | null>(null);

export function useMe(): Me {
  return useContext(SessionContext)!.me;
}

export function useReloadMe(): () => void {
  return useContext(SessionContext)!.reload;
}

const HOME: Record<Role, string> = { guard: "/kpp", admin: "/admin", advisor: "/advisor", viewer: "/report" };

const NAV: { to: string; label: string; roles: Role[] }[] = [
  { to: "/kpp", label: "КПП", roles: ["guard", "admin", "viewer"] },
  { to: "/advisor", label: "Эдвайзери", roles: ["advisor", "admin", "viewer"] },
  { to: "/report", label: "Отчёты", roles: ["admin", "viewer"] },
  { to: "/admin", label: "Управление", roles: ["admin"] },
];

function readCachedMe(): Me | null {
  try {
    return JSON.parse(localStorage.getItem(ME_CACHE) ?? "null");
  } catch {
    return null;
  }
}

export default function App() {
  // undefined — ещё грузим, null — не вошли
  const [me, setMe] = useState<Me | null | undefined>(undefined);

  const load = useCallback(() => {
    api<Me>("/api/me")
      .then((m) => {
        setMe(m);
        try {
          localStorage.setItem(ME_CACHE, JSON.stringify(m));
        } catch {
          /* не критично */
        }
      })
      .catch((e) => {
        if (e instanceof ApiError) setMe(null);
        else setMe(readCachedMe()); // нет связи: КПП продолжает работать по последнему входу
      });
  }, []);

  useEffect(load, [load]);

  if (me === undefined) return <div className="page muted">Загрузка…</div>;

  if (me === null) {
    if (webApp()) {
      return (
        <div className="page">
          <div className="card">
            Этот Telegram не подключён к журналу. Попросите у администратора ссылку-приглашение и откройте её.
          </div>
        </div>
      );
    }
    return (
      <Routes>
        <Route path="*" element={<Login onLogin={load} />} />
      </Routes>
    );
  }

  const allow = (roles: Role[], el: ReactNode) => (roles.includes(me.role) ? el : <Navigate to={HOME[me.role]} replace />);

  return (
    <SessionContext.Provider value={{ me, reload: load }}>
      <Routes>
        <Route path="/" element={<Navigate to={HOME[me.role]} replace />} />
        <Route path="/login" element={<Navigate to={HOME[me.role]} replace />} />
        <Route path="/kpp" element={allow(["guard", "admin", "viewer"], <Kpp />)} />
        <Route path="/advisor" element={allow(["advisor", "admin", "viewer"], <Advisor />)} />
        <Route path="/report" element={allow(["admin", "viewer"], <Reports />)} />
        <Route path="/admin/*" element={allow(["admin"], <Admin />)} />
        <Route path="*" element={<Navigate to={HOME[me.role]} replace />} />
      </Routes>
    </SessionContext.Provider>
  );
}

export function TopBar({ title, children }: { title: string; children?: ReactNode }) {
  const me = useMe();
  const reload = useReloadMe();
  const navigate = useNavigate();
  const links = NAV.filter((n) => n.roles.includes(me.role));

  const logout = async () => {
    await api("/api/auth/logout", { method: "POST" }).catch(() => undefined);
    try {
      localStorage.removeItem(ME_CACHE);
    } catch {
      /* не критично */
    }
    navigate("/");
    reload();
  };

  return (
    <header className="topbar">
      <h1>{title}</h1>
      {children}
      {links.length > 1 && (
        <nav>
          {links.map((l) => (
            <NavLink key={l.to} to={l.to}>
              {l.label}
            </NavLink>
          ))}
        </nav>
      )}
      {!webApp() && (
        <>
          <span className="muted hide-sm">{me.display_name}</span>
          <button className="btn small" onClick={logout}>
            Выйти
          </button>
        </>
      )}
    </header>
  );
}
