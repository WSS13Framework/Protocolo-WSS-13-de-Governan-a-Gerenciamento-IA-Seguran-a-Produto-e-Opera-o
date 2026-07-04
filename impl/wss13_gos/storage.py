"""Camada de persistência.

Dois repositórios com a mesma interface:
- InMemoryRepository: para testes e simulação.
- SQLiteRepository: persistência real em arquivo (GovernanceDB/RiskRegisterDB/EvidenceDB…).

Interface esperada pelos motores:
    save_request(request) / get_request(id)
    save_risk(assessment)
    save_approval(flow)
    save_evidence(record) / last_evidence_hash() / all_evidence()
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime

from .enums import ApprovalStatus, ExecutionStatus, RequestType, RiskLevel, Role
from .models import (
    ApprovalDecision,
    ApprovalFlow,
    EvidenceRecord,
    GovernanceRequest,
    RiskAssessment,
)


class InMemoryRepository:
    def __init__(self) -> None:
        self.requests: dict[str, GovernanceRequest] = {}
        self.risks: dict[str, RiskAssessment] = {}
        self.approvals: dict[str, ApprovalFlow] = {}
        self.evidence: list[EvidenceRecord] = []

    def save_request(self, request: GovernanceRequest) -> None:
        self.requests[request.request_id] = request

    def get_request(self, request_id: str) -> GovernanceRequest | None:
        return self.requests.get(request_id)

    def save_risk(self, assessment: RiskAssessment) -> None:
        self.risks[assessment.risk_id] = assessment

    def save_approval(self, flow: ApprovalFlow) -> None:
        self.approvals[flow.approval_flow_id] = flow

    def save_evidence(self, record: EvidenceRecord) -> None:
        self.evidence.append(record)

    def last_evidence_hash(self) -> str | None:
        return self.evidence[-1].content_hash if self.evidence else None

    def all_evidence(self) -> list[EvidenceRecord]:
        return list(self.evidence)


class SQLiteRepository:
    def __init__(self, path: str = "wss13_gos.db") -> None:
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS governance_requests (
                request_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS risk_assessments (
                risk_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS approval_flows (
                approval_flow_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS evidence (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                evidence_id TEXT UNIQUE NOT NULL,
                request_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                description TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                audit_relevant INTEGER NOT NULL
            );
            """
        )
        self._conn.commit()

    # --- serialização auxiliar ----------------------------------------------
    @staticmethod
    def _dump(obj) -> str:
        def default(o):
            if isinstance(o, datetime):
                return o.isoformat()
            if hasattr(o, "value"):  # Enum
                return o.value
            raise TypeError(f"não serializável: {type(o)}")

        return json.dumps(asdict(obj), default=default)

    # --- requests ------------------------------------------------------------
    def save_request(self, request: GovernanceRequest) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO governance_requests(request_id, payload) VALUES (?, ?)",
            (request.request_id, self._dump(request)),
        )
        self._conn.commit()

    def get_request(self, request_id: str) -> GovernanceRequest | None:
        row = self._conn.execute(
            "SELECT payload FROM governance_requests WHERE request_id = ?", (request_id,)
        ).fetchone()
        if not row:
            return None
        data = json.loads(row["payload"])
        return self._request_from_dict(data)

    @staticmethod
    def _request_from_dict(data: dict) -> GovernanceRequest:
        data = dict(data)
        data["request_type"] = RequestType(data["request_type"])
        data["status"] = ExecutionStatus(data["status"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return GovernanceRequest(**data)

    def save_risk(self, assessment: RiskAssessment) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO risk_assessments(risk_id, request_id, payload) VALUES (?, ?, ?)",
            (assessment.risk_id, assessment.request_id, self._dump(assessment)),
        )
        self._conn.commit()

    def save_approval(self, flow: ApprovalFlow) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO approval_flows(approval_flow_id, request_id, payload) "
            "VALUES (?, ?, ?)",
            (flow.approval_flow_id, flow.request_id, self._dump(flow)),
        )
        self._conn.commit()

    # --- evidence ------------------------------------------------------------
    def save_evidence(self, record: EvidenceRecord) -> None:
        self._conn.execute(
            "INSERT INTO evidence(evidence_id, request_id, event_type, actor, timestamp, "
            "description, content_hash, audit_relevant) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                record.evidence_id,
                record.request_id,
                record.event_type,
                record.actor,
                record.timestamp.isoformat(),
                record.description,
                record.content_hash,
                int(record.audit_relevant),
            ),
        )
        self._conn.commit()

    def last_evidence_hash(self) -> str | None:
        row = self._conn.execute(
            "SELECT content_hash FROM evidence ORDER BY seq DESC LIMIT 1"
        ).fetchone()
        return row["content_hash"] if row else None

    def all_evidence(self) -> list[EvidenceRecord]:
        rows = self._conn.execute("SELECT * FROM evidence ORDER BY seq ASC").fetchall()
        return [
            EvidenceRecord(
                evidence_id=r["evidence_id"],
                request_id=r["request_id"],
                event_type=r["event_type"],
                actor=r["actor"],
                timestamp=datetime.fromisoformat(r["timestamp"]),
                description=r["description"],
                content_hash=r["content_hash"],
                audit_relevant=bool(r["audit_relevant"]),
            )
            for r in rows
        ]

    def close(self) -> None:
        self._conn.close()
