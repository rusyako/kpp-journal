import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { api, ApiError, OfflineError } from "./api";
import { initData } from "./telegram";

vi.mock("./telegram", () => ({ initData: vi.fn(() => "") }));

const fetchMock = vi.fn();

beforeEach(() => {
  vi.stubGlobal("fetch", fetchMock);
  vi.mocked(initData).mockReturnValue("");
});

afterEach(() => {
  fetchMock.mockReset();
  vi.unstubAllGlobals();
});

describe("API file responses", () => {
  it("returns file bytes with cookie authentication", async () => {
    fetchMock.mockResolvedValue(new Response("xlsx-bytes"));
    const result = await api("/api/reports/2026-10-29/xlsx", { responseType: "blob" });
    expect(await result.text()).toBe("xlsx-bytes");
    const [path, options] = fetchMock.mock.calls[0];
    expect(path).toBe("/api/reports/2026-10-29/xlsx");
    expect(options.credentials).toBe("same-origin");
    expect(options).not.toHaveProperty("responseType");
  });

  it("includes Telegram authentication for file downloads", async () => {
    vi.mocked(initData).mockReturnValue("signed-init-data");
    fetchMock.mockResolvedValue(new Response("xlsx-bytes"));
    await api("/report", { responseType: "blob" });
    expect(fetchMock.mock.calls[0][1].headers.get("X-Telegram-Init-Data")).toBe("signed-init-data");
  });

  it("rejects an API error instead of downloading it as an Excel file", async () => {
    fetchMock.mockResolvedValue(new Response(JSON.stringify({ detail: "Access denied" }), { status: 403 }));
    await expect(api("/report", { responseType: "blob" })).rejects.toMatchObject({
      status: 403,
      message: "Access denied",
    });
  });

  it("preserves non-JSON errors", async () => {
    fetchMock.mockResolvedValue(new Response("Unavailable", { status: 503, statusText: "Service Unavailable" }));
    await expect(api("/report", { responseType: "blob" })).rejects.toBeInstanceOf(ApiError);
  });

  it("reports network failures", async () => {
    fetchMock.mockRejectedValue(new TypeError("Failed to fetch"));
    await expect(api("/report", { responseType: "blob" })).rejects.toBeInstanceOf(OfflineError);
  });

  it("keeps existing JSON requests and responses unchanged", async () => {
    fetchMock.mockResolvedValue(new Response(JSON.stringify({ ok: true })));
    expect(await api("/action", { method: "POST", json: { value: 1 } })).toEqual({ ok: true });
    const options = fetchMock.mock.calls[0][1];
    expect(options.body).toBe('{"value":1}');
    expect(options.headers.get("Content-Type")).toBe("application/json");
    expect(options).not.toHaveProperty("json");
  });
});
