// Копия backend/app/services/search.py (Ф-4 … Ф-7): поиск идёт в браузере при наборе.
import { words } from "./normalize";

export const SEARCH_LIMIT = 5;
export const HINT_TOO_SHORT = "Введите хотя бы 2 буквы";
export const HINT_NOT_FOUND = "Никого не найдено";
export const hintMoreLetters = (limit: number) => `Найдено больше ${limit} — введите больше букв`;

export interface Candidate {
  id: number;
  full_name: string;
  exited: boolean;
}

export interface SearchResult<T extends Candidate> {
  items: T[];
  total: number;
  hint: string | null;
}

const prefixMatch = (q: string[], name: string[]) => q.every((w) => name.some((n) => n.startsWith(w)));
const substringMatch = (q: string[], name: string[]) => q.every((w) => name.some((n) => n.includes(w)));

function compareWords(a: string[], b: string[]): number {
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (a[i] !== b[i]) return a[i] < b[i] ? -1 : 1;
  }
  return a.length - b.length;
}

export function search<T extends Candidate>(query: string, students: T[], limit = SEARCH_LIMIT): SearchResult<T> {
  const q = words(query);
  if (q.join("").length < 2) return { items: [], total: 0, hint: HINT_TOO_SHORT };

  const indexed = students.map((s) => ({ s, name: words(s.full_name) }));
  let found = indexed.filter(({ name }) => prefixMatch(q, name));
  if (found.length === 0) found = indexed.filter(({ name }) => substringMatch(q, name));

  // Сначала не вышедшие, потом фамилия, потом имя
  found.sort((a, b) => Number(a.s.exited) - Number(b.s.exited) || compareWords(a.name, b.name));

  const hint = found.length === 0 ? HINT_NOT_FOUND : found.length > limit ? hintMoreLetters(limit) : null;
  return { items: found.slice(0, limit).map((f) => f.s), total: found.length, hint };
}
