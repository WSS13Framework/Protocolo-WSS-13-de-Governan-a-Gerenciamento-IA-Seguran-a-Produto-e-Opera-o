"""Modelos de domínio (STRUCTs do documento mestre, seção 3 e apêndices)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .enums import (
    ApprovalStatus,
    ExecutionStatus,
    RequestType,
    RiskLevel,
    Role,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class GovernanceRequest:
    """STRUCT GovernanceRequest — o objeto central que percorre o pipeline."""

    request_id: str
    request_type: RequestType
    title: str
    description: str = ""
    source_channel: str = "internal"
    requester: str = "system"
    owner: str = "system"
    department: str = "unassigned"

    # Vínculos
    client_id: str | None = None
    product_id: str | None = None
    agent_id: str | None = None
    vendor_id: str | None = None

    # Flags de triagem (enrich_request_flags)
    involves_ai: bool = False
    involves_personal_data: bool = False
    involves_sensitive_data: bool = False
    involves_security: bool = False
    involves_financial_impact: bool = False
    involves_external_client: bool = False
    involves_legal_contract: bool = False
    involves_api: bool = False
    involves_production_environment: bool = False

    # Priorização
    priority: str = "NORMAL"
    business_impact: int = 1
    technical_complexity: int = 1

    # Overrides opcionais de pontuação de risco (1..5). Se None, é derivado dos flags.
    probability_override: int | None = None

    status: ExecutionStatus = ExecutionStatus.CREATED
    risk_assessment_id: str | None = None
    approval_flow_id: str | None = None

    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    def touch(self) -> None:
        self.updated_at = _now()


@dataclass
class RiskAssessment:
    """STRUCT RiskAssessment — resultado do RiskEngine."""

    risk_id: str
    request_id: str

    ai_risk_score: int
    data_risk_score: int
    security_risk_score: int
    legal_risk_score: int
    financial_risk_score: int
    operational_risk_score: int
    reputation_risk_score: int
    client_impact_score: int
    probability_score: int
    impact_score: int

    raw_score: float
    total_score: float  # normalizado 0..100
    risk_level: RiskLevel

    required_controls: list[str] = field(default_factory=list)
    required_approvers: list[Role] = field(default_factory=list)
    requires_dpia: bool = False
    requires_ai_review: bool = False
    requires_security_review: bool = False
    requires_legal_review: bool = False
    requires_founder_board: bool = False

    created_at: datetime = field(default_factory=_now)


@dataclass(frozen=True)
class EvidenceRecord:
    """STRUCT EvidenceRecord — registro imutável e com hash (INVARIANT 10)."""

    evidence_id: str
    request_id: str
    event_type: str
    actor: str
    timestamp: datetime
    description: str
    content_hash: str
    audit_relevant: bool = True


@dataclass
class ApprovalDecision:
    approver: Role
    status: ApprovalStatus
    rationale: str = ""
    timestamp: datetime = field(default_factory=_now)


@dataclass
class ApprovalFlow:
    approval_flow_id: str
    request_id: str
    required_approvers: list[Role]
    decisions: list[ApprovalDecision] = field(default_factory=list)
    status: ApprovalStatus = ApprovalStatus.PENDING


@dataclass
class GovernanceResponse:
    """Resultado do pipeline WSS13_GOS_MAIN."""

    status: str  # SUCCESS | PENDING_APPROVAL | BLOCKED | NEEDS_CORRECTION | REJECTED
    request: GovernanceRequest
    reason: str = ""
    risk_assessment: RiskAssessment | None = None
    approval_flow: ApprovalFlow | None = None
