# Acceptance Test Plan

Each requirement from the subject is mapped to an acceptance test: the steps to
run it and the expected result. Status reflects the state on `main`.

Legend: ✅ Pass · 🔁 Fixed after a bug (see *Bugs* below) · 🧪 Verified this
packaging session.

## Launch & configuration (subject V)

| # | Feature | Test steps | Expected | Status |
|---|---------|-----------|----------|--------|
| T-01 | Exactly one arg | `python3 pac-man.py` with 0 or 2+ args | Clean message, no traceback, exit | ✅ |
| T-02 | Arg must be `.json` | Pass a non-`.json` file | Clean error message | ✅ |
| T-03 | Missing config file | Pass a path that does not exist | "Config file not found", no traceback | ✅ |
| T-04 | JSON **with comments** | Config with `#` comment lines | Comments ignored, config loads | 🔁 |
| T-05 | Faulty config (bad type / out-of-range) | Set `lives: "x"`, `width: 2` | Clamp to safe default, log message, continue | ✅ |
| T-06 | Unknown keys ignored | Add `foo: 1` | Key ignored, no crash | ✅ |

## Maze generation (subject V.4)

| # | Feature | Test steps | Expected | Status |
|---|---------|-----------|----------|--------|
| T-07 | External generator used as-is | Run a level | Maze rendered from `A-Maze-ing` output | ✅ |
| T-08 | Fixed seed on level 1 | Start a game | Level 1 maze is deterministic (seed 42) | ✅ |
| T-09 | Generator failure handled | Force a too-small size | Warning logged, no crash | ✅ |

## Highscore (subject V.5)

| # | Feature | Test steps | Expected | Status |
|---|---------|-----------|----------|--------|
| T-10 | Persist top 10 | Finish games, reopen | Scores survive restart, capped at 10 | ✅ |
| T-11 | Robust to file errors | Delete / corrupt the score file | Empty list, no crash | ✅ |
| T-12 | Name validation | Enter >10 chars / symbols | Truncated / restricted to allowed chars | ✅ |
| T-13 | Shown in main menu | Open main menu | Top scores displayed | ✅ |

## Gameplay (subject VI)

| # | Feature | Test steps | Expected | Status |
|---|---------|-----------|----------|--------|
| T-14 | Player moves (arrows + WASD), walls block | Drive into corridors and walls | Moves in corridors only | 🔁 |
| T-15 | 3 lives, lose on ghost touch, respawn centre | Get caught | Life lost, respawn in middle | 🔁 |
| T-16 | Eat all pacgums → win level | Clear a level | Advance to next level | ✅ |
| T-17 | Super-pacgum → ghosts edible | Eat a super-pacgum | Ghosts flee & become edible | ✅ |
| T-18 | Eat edible ghost → score + respawn | Eat a scared ghost | Points added, ghost returns to spawn | ✅ |
| T-19 | Ghost chase behaviour | Observe ghosts | Ghosts pursue via strategy | 🔁 |
| T-20 | Scoring (pacgum/super/ghost), never decreases | Play | Score rises per config points | ✅ |
| T-21 | Level time limit | Let the timer run out | Configured end-of-time behaviour | ✅ |
| T-22 | Pause / resume | Press pause in-game | Game pauses and resumes | ✅ |

## Cheat mode (subject VI.5)

| # | Feature | Test steps | Expected | Status |
|---|---------|-----------|----------|--------|
| T-23 | Invincibility | Toggle cheat, touch ghost | No life lost | ✅ |
| T-24 | Level skip | Toggle cheat | Current level won immediately | ✅ |

## UI (subject VI.8)

| # | Feature | Test steps | Expected | Status |
|---|---------|-----------|----------|--------|
| T-25 | Main menu (Start / Highscores / Instructions / Exit) | Open menu | All entries work | ✅ |
| T-26 | HUD (score, lives, level, time) | During play | All values visible & updating | ✅ |
| T-27 | Game-over & victory screens + name entry | Win and lose | Final score shown, name saved | ✅ |

## Packaging (subject VII)

| # | Feature | Test steps | Expected | Status |
|---|---------|-----------|----------|--------|
| T-28 | Build succeeds | `make build` | `dist/pacman/` produced with bundled assets | 🧪 |
| T-29 | Frozen app loads sprites | Run the built binary | No "sprites not found" error | 🧪 🔁 |
| T-30 | Highscores persist next to the executable | Play the packaged build | Score written outside the read-only bundle | 🧪 |

## Bugs found & fixed

| Bug | Symptom | Fix (commit) |
|-----|---------|--------------|
| Parser dropped commented JSON | Config with `#` lines failed | `corrected bug on parsing with comments` (Jul 1); `Fix bug on parsing` (Jul 11) |
| Coordinate x/y ↔ line/col inversion | Entities drawn in wrong cells | `error invert x y line col` → `converter fixed` (Jul 4–5) |
| Diagonal ghost movement | Ghosts cut corners | `fix movement diag phantom` (Jul 5) |
| Retreat / strategy switching | Edible ghosts misbehaved | `retreat bug not fixed` → `fix retreat` (Jul 8–9) |
| Ghost spawn position | Ghosts spawned off-centre | `Fix spawn of ghost to the middle` (Jul 11) |
| Frozen build: sprites not found | Packaged app crashed at ghost load | Resolve assets against the PyInstaller bundle (this packaging session) |

> Note: T-01–T-27 statuses are established from the code and commit history and
> the team's manual play-testing; T-28–T-30 (packaging) were verified directly
> during the packaging session.
