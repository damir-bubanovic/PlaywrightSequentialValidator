<p align="center">
  <img src="src/images/screenshot.png" alt="PlaywrightSequentialValidator run screenshot" width="auto">
</p>

---

# PlaywrightSequentialValidator

PlaywrightSequentialValidator is a **minimal Python + Playwright automation validator** designed to prove **stable, sequential browser automation** against a public AT&T BYOD device identification flow.

The project focuses on **deterministic execution**, **single-session lifecycle**, and **DOM-driven state detection**, built specifically for technical validation scenarios where consistency and guardrails matter more than scale.

It intentionally avoids retries, proxies, or parallelism.

---

## Key Features

### ✔ Single Browser Session

- One Chromium instance per run  
- One context  
- One page  
- All identifiers processed inside that same session  

No restarts between identifiers.

---

### ✔ Strict Sequential Execution

- Identifiers processed one-by-one  
- No concurrency  
- No background workers  
- No async fan-out  

Execution order is deterministic.

---

### ✔ DOM-Based Result Detection

Outcomes are derived strictly from visible DOM state:

- Invalid IMEI  
- Incompatible device  
- EID prompt  
- Forward progression (“Choose your plan”)  

No network interception.  
No response parsing.  

UI = source of truth.

---

### ✔ Immediate Abort on Unexpected State

Hard aborts occur if any of the following appear:

- Captcha / robot checks  
- Request blocked  
- Access denied  
- Service unavailable  
- Unexpected domain redirect  

A screenshot is captured automatically on abort.

---

### ✔ Stability Evidence

- Each run emits a structured JSON artifact to `output/`
- Two consecutive runs are captured in:

```
docs/runs/run-1.txt
docs/runs/run-2.txt
```

Both runs produce consistent results for identical inputs.

---

## Validation Guarantees

This project enforces:

- Single browser session per run  
- One context + one page  
- Sequential identifier processing  
- DOM-based state detection only  
- Immediate abort on unexpected UI state  
- No retries  
- No proxies  
- No parallelism  

---

## Tech Stack

- Python 3.10+  
- Playwright (Chromium)  
- Linux (tested on Linux Mint)  

---

## Project Structure

```
PlaywrightSequentialValidator/
│
├── src/
│   ├── main.py           # Entry point
│   ├── att_flow.py       # AT&T flow logic + DOM state machine
│   ├── dom_utils.py      # DOM helpers + cookie dismissal
│   ├── debug_utils.py    # Screenshot + debug capture
│   ├── results.py        # Structured JSON output
│   ├── config.py         # Environment + constants
│   └── images/           # README screenshots
│
├── docs/
│   ├── session-lifecycle.md
│   ├── stability-approach.md
│   └── runs/
│       ├── run-1.txt
│       ├── run-2.txt
│       └── README.md
│
├── output/               # Generated run artifacts (gitignored)
├── requirements.txt
└── README.md
```

---

## Local Setup

### 1. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install Playwright Chromium

```bash
python -m playwright install chromium
```

---

## Running the Validator

From project root:

```bash
python -m src.main
```

Each run will:

- Launch Chromium  
- Process all identifiers sequentially  
- Print results to stdout  
- Save structured JSON to `output/run-<timestamp>.json`  

---

## Purpose of This Project

This repository exists to demonstrate:

- Single-session browser automation  
- Deterministic sequential execution  
- DOM-driven state machines  
- Hard failure guardrails  
- Stability across repeated runs  

It is intentionally minimal and validation-focused.

No frontend.  
No database.  
No orchestration layers.  

Just controlled browser automation.

---

## Author

**Damir Bubanović**

- Website: https://damirbubanovic.com  
- GitHub: https://github.com/damir-bubanovic  
- YouTube: https://www.youtube.com/@damirbubanovic6608  

---

## License

MIT License
