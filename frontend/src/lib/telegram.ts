// Telegram Mini App: SDK подгружается только на странице эдвайзера.

interface TelegramWebApp {
  initData: string;
  ready(): void;
  expand(): void;
  colorScheme?: "light" | "dark";
}

declare global {
  interface Window {
    Telegram?: { WebApp?: TelegramWebApp };
  }
}

export function webApp(): TelegramWebApp | null {
  const app = window.Telegram?.WebApp;
  return app && app.initData ? app : null;
}

export function initData(): string {
  return webApp()?.initData ?? "";
}

export function loadTelegramSdk(): Promise<void> {
  if (window.Telegram?.WebApp) return Promise.resolve();
  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = "https://telegram.org/js/telegram-web-app.js";
    script.onload = () => resolve();
    script.onerror = () => resolve(); // вне Telegram или без сети — работаем как обычная страница
    document.head.appendChild(script);
  });
}
