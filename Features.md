# PlaywrightSequentialValidator — Project Roadmap (Python + Playwright)

PlaywrightSequentialValidator is a minimal Python + Playwright validator that runs a public BYOD device identification flow in a **single browser session** and processes **5–10 identifiers sequentially** with **DOM-based result detection** and **hard aborts on unexpected state**.

This roadmap breaks work into clear chapters with deliverables and commit points.

---

## ✅ Completed Chapters

### Chapter 1 — Repo & Local Environment
- Git repository initialized and connected to GitHub
- `.gitignore` configured (no `.venv`, no `.idea`)
- PyCharm project created

Deliverables:
- Clean Git history going forward
- Repo ready for code

---

## 📌 To-Do Chapters

### Chapter 2 — Project Structure & Baseline Docs
- Create base folders:
  - `src/`
  - `docs/`
  - `output/` (gitignored, optional)
- Add baseline docs:
  - `README.md` (purpose, how to run)
  - `docs/session-lifecycle.md` (single-session strategy)
  - `docs/stability-approach.md` (what we enforce + why)
- Add `Features.md` (this file)

Deliverables:
- Standard repo layout
- Minimal documentation skeleton

---

### Chapter 3 — Dependencies & Playwright Setup
- Ensure venv interpreter is active in project
- Add dependencies:
  - `playwright`
- Install browser binaries:
  - `python -m playwright install chromium`
- Add `requirements.txt`

Deliverables:
- Reproducible environment
- Verified Playwright install

---

### Chapter 4 — Script Skeleton (Single Session + Sequential Loop)
- Add `src/main.py` with:
  - Config (URL, timeouts, headless toggle)
  - Single `browser` + single `context` + single `page`
  - Sequential loop over identifiers (5–10)
  - Per-identifier logging + timestamps
  - Hard abort handler (unexpected state → exit non-zero)

Deliverables:
- Runnable skeleton producing deterministic console output

---

### Chapter 5 — DOM-Based Result Detection
- Implement result detection strictly via DOM:
  - Explicit selectors for expected page states
  - A single “result extraction” function that:
    - detects success state
    - detects known failure state(s)
    - detects unknown state → abort immediately
- No retries, no parallelism, no proxy settings

Deliverables:
- Reliable DOM state machine for outcomes

---

### Chapter 6 — Stability Hardening (No Degradation Across Sequential Runs)
- Add defenses against session drift:
  - consistent navigation/reset per iteration
  - clear-field + retype input strategy
  - wait-for-state strategy (explicit timeouts)
  - guardrails: unexpected modal/captcha/error → abort
- Add structured output:
  - stdout summary table-like lines
  - optional `output/run-YYYYMMDD-HHMMSS.json` (gitignored)

Deliverables:
- Same inputs → consistent outputs across consecutive runs

---

### Chapter 7 — Two Consecutive Runs Evidence
- Run the script twice back-to-back
- Save console output for both runs under `docs/runs/`:
  - `docs/runs/run-1.txt`
  - `docs/runs/run-2.txt`
- Add short comparison note in `docs/runs/README.md`

Deliverables:
- Proof of stability across two consecutive runs

---

### Chapter 8 — Final Deliverables & Polish
- Ensure `README.md` includes:
  - setup
  - run instructions
  - constraints (no proxies/retries/parallelism)
- Confirm script exits:
  - `0` on full success
  - non-zero on abort/unexpected state
- Optional: add `Makefile` targets:
  - `make setup`
  - `make run`

Deliverables:
- Client-ready repo with clear instructions and artifacts

---

## Git Workflow

- `main` (stable)
- `feature/chapter-<n>-<slug>`

Each chapter ends with a commit:
- `Chapter <n> — <Chapter Name>`

If a chapter has major checkpoints, commit in smaller slices:
- `Chapter <n>.<k> — <Checkpoint Name>`
