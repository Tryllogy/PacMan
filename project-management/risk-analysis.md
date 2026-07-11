# Risk Analysis

Risks identified at project start, with likelihood/impact and the mitigation put
in place. Risks marked **⚠ materialized** actually occurred during development —
the corresponding commits are cited as evidence.

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|----|------|-----------|--------|-----------|--------|
| R-01 | External `A-Maze-ing` package has an unstable/unknown interface and will be **re-installed at peer review** | Medium | High | Write a thin loader that adapts to *their* interface; never modify the package; handle generation failure cleanly | Contained |
| R-02 | Ghost AI (chase + retreat) is the hardest part and may not converge | High | High | Isolate behaviour behind swappable `Strategy` classes; iterate; keep a simpler random strategy as fallback | ⚠ **Materialized** |
| R-03 | Grid ↔ pixel coordinate confusion (row/col vs x/y) | Medium | Medium | Centralise all conversions in a single `Converter` class | ⚠ **Materialized** |
| R-04 | Config file is untrusted (bad values, comments, missing keys, wrong type) | High | Medium | JSON5 parsing + Pydantic validation with clamped defaults; ignore unknown keys; never crash | Contained |
| R-05 | Packaged build behaves differently from `python3 pac-man.py` (asset paths, deps) | Medium | High | Bundle assets via PyInstaller `--add-data`; resolve paths against the bundle at runtime | ⚠ **Materialized** |
| R-06 | Merge conflicts between the rendering branch and the AI branch | High | Low | Split ownership by module; merge often in small increments | Contained |
| R-07 | Maze too small for the configured seed / entities | Low | Medium | Enforce minimum level size (`width`/`height` ≥ 10) in config validation; log a warning and continue | Contained |
| R-08 | Unhandled exception crashes the game during review ("non-functional") | Medium | High | `try/except` around parsing and the top-level `main`; context managers for files | Contained |

## Notes on materialized risks

- **R-02 (Ghost AI).** The retreat/flee behaviour needed several passes —
  `retreat ok but switching strat bug` → `retreat bug not fixed` → `fix retreat`
  (Jul 8–9). Mitigation worked: strategies were swappable, so debugging one did
  not destabilise the others, and the random strategy remained a safety net.

- **R-03 (Coordinates).** Explicitly hit in `error invert x y line col` (Jul 4),
  resolved by `converter fixed` (Jul 5). Concentrating the math in `Converter`
  meant a single fix corrected every entity's placement.

- **R-05 (Packaging).** After the first PyInstaller build, sprites failed to load
  in the frozen app because the sprite directory was resolved by a relative path
  instead of against the bundle. Fixed by resolving assets against
  `sys._MEIPASS` (bundle) and writable data next to the executable, and by
  switching the build to `--onedir` for a cleaner Itch.io distribution.
