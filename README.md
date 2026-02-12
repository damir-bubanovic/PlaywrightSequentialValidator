# PlaywrightSequentialValidator

Minimal Python + Playwright validator that processes multiple test identifiers **sequentially** in a **single browser session**.

## Constraints (by design)

- Single session only  
- Sequential execution only  
- DOM-based result detection  
- Immediate abort on unexpected state  
- No proxies, no retries, no parallelism  


## Validation Guarantees

This project enforces:

- Single browser session per run
- One context + one page
- Sequential identifier processing
- DOM-based state detection only
- Immediate abort on unexpected UI state
- No retries, no proxies, no parallelism

Each run also emits a structured JSON artifact under `output/`.
Two consecutive run logs are provided in `docs/runs/`.


## Repo Layout

- `src/` – automation code  
- `docs/` – session lifecycle, stability notes, run outputs  
- `docs/runs/` – evidence from consecutive runs  

## Quickstart (after dependencies)

```bash
python -m playwright install chromium
python src/main.py
```