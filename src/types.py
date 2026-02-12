from dataclasses import dataclass


@dataclass(frozen=True)
class Outcome:
    kind: str  # e.g. OK / NEEDS_EID / INVALID / INCOMPATIBLE
    details: str  # human-readable summary
