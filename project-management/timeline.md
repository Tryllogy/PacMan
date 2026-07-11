# Timeline & Progress Tracking

The project ran for **three weeks**, from **2026-06-21** to **2026-07-11**
(75 commits on `main`). Work was organised into three phases, each ending on a
functional milestone.

## Phase breakdown (as executed)

### Phase 1 — Foundations (Jun 21 → Jun 26)
Goal: project skeleton, tooling, and the two "input" systems (config + maze).

- Repo bootstrap: `config.json`, `Makefile`, `pyproject.toml`, `TODO`, sprites *(tchemin, Jun 21)*
- JSON5 config parsing + Pydantic validation with defaults and extra-key rejection *(jsam, Jun 23–26)*
- Main menu + reusable buttons *(tchemin, Jun 24)*
- `A-Maze-ing` maze generator integration *(jsam, Jun 26)*
- Config wired into `main`; first maze drawing *(tchemin, Jun 26)*

**Milestone:** the game boots, parses a config, and generates a maze. ✅

### Phase 2 — Core gameplay & rendering (Jun 27 → Jul 2)
Goal: a playable board — maze, entities, movement, scenes, scoring.

- Maze rendering; pacgums & super-pacgums; phantom sprites *(tchemin, Jun 27)*
- BFS pathfinding (`build_path` / `rev_path`) + algorithm testing *(jsam, Jun 27)*
- Scene management: instructions, scoreboard, pause; JSON permission check *(jsam, Jun 28–29)*
- Player movement; pacman drawn in-game *(tchemin, Jun 29)*
- Phantom movement & on-screen placement by maze cell *(jsam, Jun 30 → Jul 1)*
- Levels config, lives + score, win/lose switch, timer; parser comment bugfix *(tchemin, Jul 1)*
- `Converter` (grid ↔ pixel) class; `Score` class; `EndScene` refactor; `zone_strategy` *(both, Jul 2)*

**Milestone:** a full level is playable start-to-finish with scoring and end screens. ✅

### Phase 3 — AI polish, cheat mode & packaging (Jul 4 → Jul 11)
Goal: correct ghost AI, evaluation tooling, quality gate, and a deliverable build.

- Coordinate `x/y` (line/col) inversion fixed; diagonal-movement fix *(jsam, Jul 4–5)*
- Cheat mode (invincibility + level skip); respawn on death; name-input hardening *(tchemin, Jul 7)*
- Aggressive & random strategies fixed; **retreat** behaviour (several iterations) *(jsam, Jul 7–9)*
- Eating ghosts + return-to-spawn; dead/scared sprites; dead-code cleanup; `flake8` *(tchemin, Jul 9)*
- Parser bugfix + WASD controls; `mypy` fix; ghost spawn-to-centre fix; **PyInstaller build** *(tchemin, Jul 11)*

**Milestone:** feature-complete, lint-clean, and packaged for distribution. ✅

## Gantt (weekly)

```
Task \ Week                     W1 (06-21)  W2 (06-27)  W3 (07-04)
Tooling & repo setup            ####
Config parsing & validation     ######
Maze generator integration        ####
Menus / scenes / UI             ##########  ####
Maze & entity rendering            #######
Player movement                       #####
Ghost pathfinding & strategies        ###########  #########
Coordinate converter                     ####  ####
Scoring / lives / timer               ######
Win / Lose / End screens              ######
Cheat mode                                       ####
Sprites (dead / scared / rework)                 #####
Linting (flake8 + mypy)                      #   #####
Packaging (PyInstaller)                              ####
```

## Actual progress vs. plan

| Area | Planned | Actual | Note |
|------|---------|--------|------|
| Foundations (config, maze, menu) | Week 1 | Week 1 | On schedule |
| Core gameplay & rendering | Week 2 | Week 2 | On schedule |
| Ghost AI (chase/retreat) | Week 2 | Weeks 2–3 | **Slipped** — retreat logic needed several iterations (see [risk-analysis.md](risk-analysis.md) R-02 and [retrospective.md](retrospective.md)) |
| Cheat mode & polish | Week 3 | Week 3 | On schedule |
| Packaging | Week 3 | Week 3 (last day) | Delivered; a path-resolution bug in the frozen build was fixed post-packaging |

**Main deviation:** ghost AI — especially the *retreat* (edible/flee) behaviour and
the maze coordinate mapping — absorbed noticeably more time than planned. The
commit trail (`retreat ok but switching strat bug` → `retreat bug not fixed` →
`fix retreat`) documents the debugging effort. This was an anticipated risk and
did not endanger the final delivery.
