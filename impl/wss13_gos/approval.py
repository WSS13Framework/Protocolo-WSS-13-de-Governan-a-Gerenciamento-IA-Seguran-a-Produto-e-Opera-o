"""ApprovalEngine — motor de aprovação por alçadas (seção 8)."""

from __future__ import annotations

from typing import Callable

from .enums import ApprovalStatus, ExecutionStatus, Role
from .evidence import EvidenceVault
from .ids import IDGenerator
from .models import ApprovalDecision, ApprovalFlow, GovernanceRequest, RiskAssessment

# Um "resolvedor" de decisão recebe (aprovador, request, assessment) e devolve uma decisão.
DecisionResolver = Callable[[Role, GovernanceRequest, RiskAssessment], ApprovalDecision]


def auto_approve(approver: Role, request: GovernanceRequest,
                 assessment: RiskAssessment) -> ApprovalDecision:
    """Resolvedor padrão para simulação/testes: aprova tudo."""
    return ApprovalDecision(approver=approver, status=ApprovalStatus.APPROVED,
                            rationale="auto-approved (simulation)")


class ApprovalEngine:
    def __init__(self, ids: IDGenerator, repository, evidence: EvidenceVault) -> None:
        self._ids = ids
        self._repo = repository
        self._evidence = evidence

    def route(self, request: GovernanceRequest, assessment: RiskAssessment,
              resolver: DecisionResolver = auto_approve) -> ApprovalFlow:
        flow = ApprovalFlow(
            approval_flow_id=self._ids.create("WSS13-APR"),
            request_id=request.request_id,
            required_approvers=list(assessment.required_approvers),
        )

        for approver in assessment.required_approvers:
            decision = resolver(approver, request, assessment)
            flow.decisions.append(decision)
            self._evidence.record(
                request_id=request.request_id,
                event_type="APPROVAL_DECISION",
                actor=approver.value,
                description=f"{decision.status.value} by {approver.value}",
            )
            if decision.status == ApprovalStatus.REJECTED:
                flow.status = ApprovalStatus.REJECTED
                request.status = ExecutionStatus.REJECTED
                self._persist(request, flow)
                return flow
            if decision.status == ApprovalStatus.NEEDS_REVIEW:
                flow.status = ApprovalStatus.NEEDS_REVIEW
                request.status = ExecutionStatus.WAITING_APPROVAL
                self._persist(request, flow)
                return flow

        flow.status = ApprovalStatus.APPROVED
        request.status = ExecutionStatus.APPROVED
        request.approval_flow_id = flow.approval_flow_id
        self._persist(request, flow)
        return flow

    def _persist(self, request: GovernanceRequest, flow: ApprovalFlow) -> None:
        request.touch()
        self._repo.save_request(request)
        self._repo.save_approval(flow)
