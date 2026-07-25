"""Orquestrador — equivalente a WSS13_GOS_MAIN (seção 4).

Encadeia Intake → Triage → Risk → Approval, gerando evidência a cada etapa e
respeitando os invariantes do protocolo (nada executa sem avaliação de risco;
nada é aprovado sem passar por todos os aprovadores exigidos).
"""

from __future__ import annotations

from .approval import ApprovalEngine, DecisionResolver, auto_approve
from .audit import AuditEngine
from .enums import ApprovalStatus, ExecutionStatus
from .evidence import EvidenceVault
from .ids import IDGenerator
from .incident import IncidentEngine
from .intake import IntakeEngine, TriageEngine
from .metrics import MetricsEngine
from .models import GovernanceResponse
from .risk import RiskEngine
from .storage import InMemoryRepository


class GovernanceOrchestrator:
    """MODULE WSS13_GOS — compõe os motores sobre um repositório."""

    def __init__(self, repository=None) -> None:
        self.repo = repository or InMemoryRepository()
        self.ids = IDGenerator()
        self.evidence = EvidenceVault(self.ids, self.repo)
        self.intake = IntakeEngine(self.ids, self.repo)
        self.triage = TriageEngine(self.repo)
        self.risk = RiskEngine(self.ids, self.repo)
        self.approval = ApprovalEngine(self.ids, self.repo, self.evidence)
        self.incidents = IncidentEngine(self.ids, self.repo, self.evidence)
        self.audit = AuditEngine(self.ids, self.repo, self.evidence)
        self.metrics = MetricsEngine(self.repo, self.evidence)

    def execute(self, event: dict,
                resolver: DecisionResolver = auto_approve) -> GovernanceResponse:
        # 1. Intake
        request = self.intake.register(event)
        self.evidence.record(request.request_id, "REQUEST_CREATED",
                             request.requester, "New governance request registered.")

        # 2. Triage
        triage = self.triage.classify(request)
        self.evidence.record(request.request_id, "REQUEST_TRIAGED", "SYSTEM", triage["summary"])

        # 3. Risk (INVARIANT 2: nada executa sem avaliação de risco)
        assessment = self.risk.assess(request)
        request.status = ExecutionStatus.RISK_CLASSIFIED
        self.repo.save_request(request)
        self.evidence.record(request.request_id, "RISK_ASSESSED", "SYSTEM",
                             f"Risk level: {assessment.risk_level.value} "
                             f"(score {assessment.total_score})")

        # 4. Approval por alçadas
        flow = self.approval.route(request, assessment, resolver)
        if flow.status == ApprovalStatus.REJECTED:
            return GovernanceResponse("REJECTED", request, "Approval rejected.",
                                      assessment, flow)
        if flow.status != ApprovalStatus.APPROVED:
            self.evidence.record(request.request_id, "WAITING_APPROVAL", "SYSTEM",
                                 "Request waiting for required approvals.")
            return GovernanceResponse("PENDING_APPROVAL", request,
                                      "Waiting for approvals.", assessment, flow)

        # 5. Execução aprovada → fecha com evidência (execução/QA/release simplificados
        #    nesta implementação de referência da Fase 1).
        request.status = ExecutionStatus.CLOSED
        self.repo.save_request(request)
        self.evidence.record(request.request_id, "REQUEST_CLOSED", "SYSTEM",
                             "Governance process completed successfully.")
        return GovernanceResponse("SUCCESS", request, "", assessment, flow)
