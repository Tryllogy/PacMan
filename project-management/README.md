# Project Management

This directory contains the evidence of how the **Pac-Man** project was driven,
from kick-off to packaging. Everything here is reconstructed from and backed by
the project's real Git history on `main` (75 commits, 2026-06-21 → 2026-07-11,
two contributors).

## Team

| Member | 42 login | Main responsibilities |
|--------|----------|-----------------------|
| Thomas Chemin | `tchemin` | Rendering & graphics, UI/scenes, player, config plumbing, scoring, cheat mode, packaging, linting |
| Jean-Yves Sam | `jsam` | Config parsing & validation, maze-generator integration, ghost AI (pathfinding & strategies), coordinate converter |

## Approach

We used a lightweight, **feature-branch + Kanban** approach:

- Two long-lived branches (`Thomas`, `jsam`) integrated into `main` through
  regular merges — the log shows frequent `Merge remote-tracking branch` commits.
- Work was sliced into small, single-purpose commits so progress and ownership
  stay traceable in `git log`.
- A short-lived `TODO` file tracked the next actionable item during development.

## Documents

| File | Content |
|------|---------|
| [timeline.md](timeline.md) | Planned schedule, phase breakdown, Gantt, and actual progress vs. plan |
| [team-organization.md](team-organization.md) | Who did what, how decisions were made, how issues were handled |
| [risk-analysis.md](risk-analysis.md) | Identified risks, likelihood/impact, and mitigations (with those that materialized) |
| [acceptance-test-plan.md](acceptance-test-plan.md) | Feature-by-feature acceptance tests mapped to the subject, and bugs found/fixed |
| [retrospective.md](retrospective.md) | Blocking points, conflicts, and lessons learned |

## Tools used

- **Git** (feature branches + merges) — version control and progress evidence.
- **Kanban / TODO list** — task tracking.
- **`make lint` / `make lint-strict`** (flake8 + mypy) — continuous quality gate.
- **pytest / manual acceptance runs** — functional verification.
- **PyInstaller** — packaging for the target platform (Itch.io).
