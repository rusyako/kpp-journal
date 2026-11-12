import { useEffect, useRef } from "react";
import { initData } from "./telegram";

/**
 * Подписка на события сервера. onChange вызывается (с задержкой-склейкой) при любом изменении,
 * а также раз в минуту — на случай, если сокет тихо отвалился.
 */
export function useLiveUpdates(onChange: () => void): void {
  const handler = useRef(onChange);
  handler.current = onChange;

  useEffect(() => {
    let ws: WebSocket | null = null;
    let closed = false;
    let retry = 1000;
    let debounce: number | undefined;
    let ping: number | undefined;

    const fire = () => {
      window.clearTimeout(debounce);
      debounce = window.setTimeout(() => handler.current(), 250);
    };

    const connect = () => {
      const proto = location.protocol === "https:" ? "wss" : "ws";
      ws = new WebSocket(`${proto}://${location.host}/api/ws`);
      ws.onopen = () => {
        // Mini App входит первым сообщением, а не через адрес: адреса пишутся в журналы сервера
        const tg = initData();
        if (tg) ws?.send(`auth:${tg}`);
        retry = 1000;
        fire(); // могли пропустить события, пока не было связи
        ping = window.setInterval(() => ws?.readyState === WebSocket.OPEN && ws.send("ping"), 25000);
      };
      ws.onmessage = fire;
      ws.onclose = () => {
        window.clearInterval(ping);
        if (!closed) window.setTimeout(connect, (retry = Math.min(retry * 2, 30000)));
      };
    };

    connect();
    const poll = window.setInterval(fire, 60000);
    const onVisible = () => document.visibilityState === "visible" && fire();
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      closed = true;
      ws?.close();
      window.clearInterval(poll);
      window.clearInterval(ping);
      window.clearTimeout(debounce);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, []);
}
