# Graph Report - kpp-journal  (2026-11-03)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 560 nodes · 1534 edges · 17 communities (13 shown, 4 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2077ee77`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Permissions API, Models & Migrations
- Students, Import & Admin API
- Frontend Pages & API Types
- Backend Test Fixtures & Auth
- Day Sheet Statuses & Notifications
- App Entry, WebSocket & Bot
- KPP Exits, Clock & Audit
- Frontend Package Config
- Frontend Search & Normalize
- Backend Search Reference
- TypeScript Config
- Admin CLI & Demo Seed
- Login & Sessions
- Backup Script
- Repository Root

## God Nodes (most connected - your core abstractions)
1. `User` - 63 edges
2. `Student` - 28 edges
3. `apply_import()` - 24 edges
4. `api()` - 22 edges
5. `DayRow` - 21 edges
6. `Role` - 20 edges
7. `Advisory` - 20 edges
8. `mark_exit()` - 20 edges
9. `set_permission()` - 18 edges
10. `format_time()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `db()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/models.py
- `session()` --uses--> `Base`  [INFERRED]
  backend/tests/test_importer.py → backend/app/models.py
- `load_day()` --uses--> `Exit`  [INFERRED]
  backend/app/services/day.py → backend/app/models.py
- `_active_exit()` --uses--> `Exit`  [INFERRED]
  backend/app/services/exits.py → backend/app/models.py
- `build_report()` --uses--> `Exit`  [INFERRED]
  backend/app/services/report.py → backend/app/models.py

## Import Cycles
- None detected.

## Communities (17 total, 4 thin omitted)

### Community 0 - "Permissions API, Models & Migrations"
Cohesion: 0.06
Nodes (27): downgrade(), upgrade(), advisories(), advisory(), PermissionIn, put_permission(), me(), greeting() (+19 more)

### Community 1 - "Students, Import & Admin API"
Cohesion: 0.06
Nodes (56): _apply_user(), _commit_user(), create_student(), create_user(), delete_school_day(), _diff_dict(), health(), import_list() (+48 more)

### Community 2 - "Frontend Pages & API Types"
Cohesion: 0.07
Nodes (67): App(), HOME, NAV, readCachedMe(), Session, SessionContext, TopBar(), useMe() (+59 more)

### Community 3 - "Backend Test Fixtures & Auth"
Cohesion: 0.07
Nodes (29): validate_init_data(), verify_password(), admin(), advisor(), Clock, guard(), login(), now() (+21 more)

### Community 4 - "Day Sheet Statuses & Notifications"
Cohesion: 0.07
Nodes (26): UserAdvisory, advisor_chat_ids(), exit_changed(), exit_text(), report_chat_ids(), send_email(), send_telegram(), _submit() (+18 more)

### Community 5 - "App Entry, WebSocket & Bot"
Cohesion: 0.06
Nodes (14): run(), resolve_user(), day_changed(), Hub, health(), lifespan(), spa(), websocket() (+6 more)

### Community 6 - "KPP Exits, Clock & Audit"
Cohesion: 0.09
Nodes (17): audit_log(), create_exit(), day(), ExitIn, remove_exit(), _result(), now(), now_minute() (+9 more)

### Community 7 - "Frontend Package Config"
Cohesion: 0.08
Nodes (24): dependencies, react, react-dom, react-router-dom, devDependencies, @types/react, @types/react-dom, typescript (+16 more)

### Community 8 - "Frontend Search & Normalize"
Cohesion: 0.17
Nodes (15): LETTERS, normalize(), words(), Candidate, compareWords(), HINT_NOT_FOUND, HINT_TOO_SHORT, hintMoreLetters() (+7 more)

### Community 9 - "Backend Search Reference"
Cohesion: 0.24
Nodes (11): words(), Candidate, _prefix_match(), search(), SearchResult, _sort_key(), _substring_match(), test_exited_go_after_not_exited() (+3 more)

### Community 10 - "TypeScript Config"
Cohesion: 0.13
Nodes (14): compilerOptions, isolatedModules, jsx, lib, module, moduleResolution, noUnusedLocals, noUnusedParameters (+6 more)

### Community 11 - "Admin CLI & Demo Seed"
Cohesion: 0.31
Nodes (5): create_admin(), demo(), main(), hash_password(), db()

### Community 12 - "Login & Sessions"
Cohesion: 0.29
Nodes (4): login(), LoginIn, logout(), make_session()

## Knowledge Gaps
- **4 isolated node(s):** `kpp-journal`, `@types/react`, `@types/react-dom`, `typescript`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 177 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `Permissions API, Models & Migrations` to `Students, Import & Admin API`, `Backend Test Fixtures & Auth`, `Day Sheet Statuses & Notifications`, `App Entry, WebSocket & Bot`, `KPP Exits, Clock & Audit`, `Admin CLI & Demo Seed`, `Login & Sessions`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Are the 45 inferred relationships involving `User` (e.g. with `_apply_user()` and `create_student()`) actually correct?**
  _`User` has 45 INFERRED edges - model-reasoned connections that need verification._
- **What connects `kpp-journal`, `@types/react`, `@types/react-dom` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Permissions API, Models & Migrations` be split into smaller, more focused modules?**
  _Cohesion score 0.05628002745367193 - nodes in this community are weakly interconnected._
- **Why does `Student` connect `Students, Import & Admin API` to `Permissions API, Models & Migrations`, `Backend Test Fixtures & Auth`, `Day Sheet Statuses & Notifications`, `KPP Exits, Clock & Audit`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `Student` (e.g. with `create_student()` and `health()`) actually correct?**
  _`Student` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `Students, Import & Admin API` be split into smaller, more focused modules?**
  _Cohesion score 0.06128702757916241 - nodes in this community are weakly interconnected._