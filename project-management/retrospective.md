# Retrospective — Blocking Points & Conflicts

A short honest review of what slowed us down and how we got past it.

## Blocking points

### 1. Ghost AI — retreat / strategy switching (biggest blocker)
The chase strategies came together relatively quickly, but making ghosts **flee
correctly when edible** and **switch back** afterwards was hard. The history
records the struggle across several days:
`aggressiv strategy work but retreat dont` (Jun 29) → `retreat ok but switching
strat bug` → `retreat bug not fixed` (Jul 8) → `fix retreat` (Jul 9).

- **Root cause:** state transitions between strategies (chase ↔ flee ↔ return to
  spawn) were entangled with the pathfinding.
- **Resolution:** strategies were refactored into swappable classes and the
  "is retreating" flag was turned into a property, isolating the state machine.

### 2. Coordinate system (grid vs pixels)
Entities were placed using inconsistent `x/y` vs `row/col` conventions, causing
misaligned ghosts and player (`error invert x y line col`, Jul 4).

- **Resolution:** a single `Converter` class became the one source of truth for
  grid ↔ pixel translation; the fix then applied everywhere at once.

### 3. Config parsing with comments
The JSON5-with-comments requirement caused an early parsing bug that silently
fell back to defaults (`corrected bug on parsing with comments`, Jul 1; revisited
Jul 11).

### 4. Packaging path resolution (late, external)
The very last step — packaging with PyInstaller — surfaced a bug that never
appeared in development: assets were located by a **relative** path, which does
not exist inside the frozen bundle, so ghost sprites failed to load. Fixed by
resolving assets against the bundle and keeping writable data next to the
executable, and by switching to `--onedir` for distribution.

## Conflicts (technical & merge)

- Because two branches (`Thomas`, `jsam`) touched the game loop, the integration
  points produced merge conflicts (`fix conflict in_game`, multiple `merge`
  commits). They were kept small by merging often rather than in big batches.
- No process conflicts of note: ownership was split by subsystem, which kept the
  two workstreams mostly independent.

## What went well
- Clear module ownership → few, small conflicts.
- Swappable strategy classes → AI bugs stayed contained.
- A shared lint gate (flake8 + mypy) kept quality steady to the end.

## What we would do differently
- Introduce the `Converter` abstraction **from day one** to avoid the coordinate
  churn.
- Do a **trial PyInstaller build mid-project**, not on the last day, so the asset
  path issue would have surfaced early.
- Write a couple of automated tests around the ghost state machine to catch
  retreat regressions faster.
