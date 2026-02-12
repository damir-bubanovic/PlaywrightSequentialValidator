## Notes (2026-02-12)

Two consecutive runs (`run-1.txt`, `run-2.txt`) produced consistent results for the same 5 identifiers.

Stability notes:
- Single browser session per run
- Sequential processing in one page/context
- Deterministic reset per identifier via navigation back to the identify URL
- DOM-based error detection (“IMEI not found. Please try re-entering.”) captured consistently
