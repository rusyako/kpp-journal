// Копия backend/app/services/normalize.py (Ф-6). Совпадение проверяет normalize.test.ts
// на общих примерах из shared/search_cases.json.

const LETTERS: Record<string, string> = {
  ә: "а",
  ғ: "г",
  қ: "к",
  ң: "н",
  ө: "о",
  ұ: "у",
  ү: "у",
  һ: "х",
  і: "и",
  ё: "е",
};

const APOSTROPHES = /[’'`ʼ‘"«»]/g;
const SEPARATORS = /[^\p{L}\p{N}]+/gu;

export function normalize(text: string): string {
  let s = text.toLowerCase();
  s = s.replace(/[әғқңөұүһіё]/g, (ch) => LETTERS[ch]);
  s = s.replace(APOSTROPHES, "");
  return s.replace(SEPARATORS, " ").trim();
}

export function words(text: string): string[] {
  const n = normalize(text);
  return n ? n.split(" ") : [];
}
