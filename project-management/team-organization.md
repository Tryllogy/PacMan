# Team Organization

## Members and ownership

The project was built by **two developers**. Responsibilities were split by
subsystem to minimise merge conflicts and let each person own a coherent area,
while pairing on the integration seams (config → game, maze → rendering,
converter → AI).

### Thomas Chemin (`tchemin`) — Graphics, UI & game shell
- Project bootstrap: `Makefile`, `pyproject.toml`, config file, sprites.
- Rendering: maze drawing, pacgums / super-pacgums, all phantom & pacman sprites
  (including the later dead/scared sprite rework).
- UI / scenes: main menu, reusable buttons, pause menu with options,
  win/lose screens later refactored into a single `EndScene`.
- Player: movement (arrow keys + WASD), lives, respawn on death.
- Scoring: dedicated `Score` class, points wiring, in-game timer.
- Cheat mode (invincibility + level skip) for peer review.
- Quality & delivery: flake8/mypy fixes, PyInstaller packaging.

### Jean-Yves Sam (`jsam`) — Parsing, maze integration & ghost AI
- Config: JSON5 parsing and Pydantic-based validation (defaults, extra-key
  handling, file-permission checks).
- Maze: integration of the external `A-Maze-ing` package (used as-is).
- Ghost AI: BFS pathfinding (`build_path` / `rev_path`), and the movement
  strategies — aggressive (chase), random, zone, and retreat (flee when edible).
- `Converter` class translating maze grid cells ↔ screen pixels.
- Scene-management contributions (instructions & scoreboard navigation, pause
  transition while in-game).

## How decisions were made

- **Architecture by module boundaries.** Each subsystem (parsing, entities,
  scenes, strategies, converter) is a separate package/class, agreed up front so
  the two branches could evolve independently and merge cleanly.
- **Interface adaptation, not modification.** For the maze generator, the team
  decided the *loader adapts to the package's interface* (never the reverse),
  as required by the subject. The `Converter` class was introduced specifically
  to isolate the grid/pixel coordinate translation in one place after coordinate
  bugs appeared.
- **Config-driven design.** Gameplay parameters (lives, points, seed, level
  sizes, time limit) live in the JSON config with robust defaults, decided so the
  ruleset can be changed at defence time without code changes.

## Collaboration workflow

- Two feature branches (`Thomas`, `jsam`) integrated into `main` via frequent
  merges — the history shows repeated `Merge remote-tracking branch
  'origin/Thomas' into Jean-Yves` and reciprocal merges.
- Small, single-purpose commits with descriptive messages, so ownership and
  progress are auditable from `git log` / `git shortlog`.
- A running `TODO` file captured the next actionable item.

## How issues were handled

- **Merge conflicts** (e.g. `fix conflict in_game`, `merge Jean-Yves`) were
  resolved at the integration points where rendering (Thomas) met movement/AI
  (Jean-Yves).
- **Cross-cutting bugs** were assigned to the owner of the affected subsystem:
  coordinate inversion and retreat behaviour → Jean-Yves; parsing/comment and
  spawn-position bugs → Thomas.
- **Quality regressions** were caught by the shared `make lint` gate before
  merging (dedicated `flake8` and `fix mypy` commits).
