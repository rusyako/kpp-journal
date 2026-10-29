import { describe, expect, it } from "vitest";
import data from "../../../shared/search_cases.json";
import { normalize } from "./normalize";
import { search, type Candidate } from "./search";

const students = data.students as Candidate[];

describe("поиск совпадает с backend (shared/search_cases.json)", () => {
  for (const c of data.cases) {
    it(c.query, () => {
      const r = search(c.query, students);
      expect(r.items.map((s) => s.full_name)).toEqual(c.names);
      expect(r.total).toBe(c.total);
      expect(r.hint).toBe(c.hint);
    });
  }
});

describe("normalize", () => {
  it.each([
    ["Ақтілекқызы", "актилеккызы"],
    ["ӘҒҚҢӨҰҮҺІ", "агкноуухи"],
    ["Гилёва", "гилева"],
    ["Ма'руфов  Азиз", "маруфов азиз"],
    ["Абу-Бакир", "абу бакир"],
    ["  КИМ   илья ", "ким илья"],
  ])("%s", (raw, expected) => {
    expect(normalize(raw)).toBe(expected);
  });
});
