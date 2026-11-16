import { useId, useState, type ComponentProps } from "react";

export default function PasswordInput({ className = "input", id, ...props }: Omit<ComponentProps<"input">, "type">) {
  const [visible, setVisible] = useState(false);
  const generatedId = useId();
  const inputId = id ?? generatedId;
  const action = visible ? "Скрыть пароль" : "Показать пароль";

  return (
    <span className="password-input">
      <input {...props} id={inputId} className={className} type={visible ? "text" : "password"} />
      <button
        type="button"
        className="password-toggle"
        aria-label={action}
        title={action}
        aria-pressed={visible}
        aria-controls={inputId}
        disabled={props.disabled}
        onClick={() => setVisible(!visible)}
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z" />
          <circle cx="12" cy="12" r="3" />
          {visible && <path d="m3 3 18 18" />}
        </svg>
      </button>
    </span>
  );
}
