"""EvidenceVault — cofre de evidências imutável e com hash (seção 18).

Implementa INVARIANT 10: todo evento de governança gera um registro de evidência
imutável e com hash. O hash encadeia o registro anterior (estilo cadeia de blocos),
tornando adulteração detectável.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from .ids import IDGenerator
from .models import EvidenceRecord


class EvidenceVault:
    def __init__(self, ids: IDGenerator, repository) -> None:
        self._ids = ids
        self._repo = repository

    @staticmethod
    def _hash(prev_hash: str, request_id: str, event_type: str, actor: str,
              timestamp: datetime, description: str) -> str:
        payload = "|".join(
            [prev_hash, request_id, event_type, actor, timestamp.isoformat(), description]
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def record(self, request_id: str, event_type: str, actor: str,
               description: str, *, now: datetime | None = None) -> EvidenceRecord:
        now = now or datetime.now(timezone.utc)
        prev_hash = self._repo.last_evidence_hash() or "GENESIS"
        content_hash = self._hash(prev_hash, request_id, event_type, actor, now, description)
        evidence = EvidenceRecord(
            evidence_id=self._ids.create("WSS13-EVD", now=now),
            request_id=request_id,
            event_type=event_type,
            actor=actor,
            timestamp=now,
            description=description,
            content_hash=content_hash,
            audit_relevant=True,
        )
        self._repo.save_evidence(evidence)
        return evidence

    def verify_chain(self) -> bool:
        """Revalida toda a cadeia de evidências; retorna False se houver adulteração."""
        prev_hash = "GENESIS"
        for ev in self._repo.all_evidence():
            expected = self._hash(
                prev_hash, ev.request_id, ev.event_type, ev.actor, ev.timestamp, ev.description
            )
            if expected != ev.content_hash:
                return False
            prev_hash = ev.content_hash
        return True
