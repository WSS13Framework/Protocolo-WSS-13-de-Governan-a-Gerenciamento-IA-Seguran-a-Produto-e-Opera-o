"""Gerador de IDs no padrão do protocolo: PREFIX-YYYY-NNNN."""

from __future__ import annotations

import itertools
from datetime import datetime, timezone


class IDGenerator:
    """Gera identificadores sequenciais por prefixo.

    Ex.: WSS13-GOV-2026-0001, WSS13-RISK-2026-0007, WSS13-EVD-2026-0042.
    """

    def __init__(self) -> None:
        self._counters: dict[str, itertools.count] = {}

    def create(self, prefix: str, *, now: datetime | None = None) -> str:
        now = now or datetime.now(timezone.utc)
        year = now.year
        key = f"{prefix}-{year}"
        counter = self._counters.setdefault(key, itertools.count(1))
        seq = next(counter)
        return f"{prefix}-{year}-{seq:04d}"
