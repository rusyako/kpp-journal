import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { loadTelegramSdk } from "./lib/telegram";
import "./styles.css";

async function start() {
  // Mini App эдвайзера: initData должен быть готов до первого запроса
  if (location.pathname.startsWith("/advisor")) await loadTelegramSdk();

  createRoot(document.getElementById("root")!).render(
    <StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </StrictMode>,
  );

  if ("serviceWorker" in navigator && import.meta.env.PROD) {
    navigator.serviceWorker.register("/sw.js").catch(() => undefined);
  }
}

start();
