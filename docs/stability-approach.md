# Stability approach

Goals:

- Consistent output across sequential queries
- Consistent output across consecutive runs

Hard constraints:

- No proxies
- No retries
- No parallelism

Approach:

- DOM-based detection only
- Explicit timeouts
- Deterministic per-identifier reset
- Abort immediately on unknown UI state
