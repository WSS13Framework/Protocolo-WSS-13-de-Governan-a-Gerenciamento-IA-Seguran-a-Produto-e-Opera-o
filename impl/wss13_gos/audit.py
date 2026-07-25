"""AuditEngine — auditoria interna (seção 19).

Executa uma auditoria sobre os dados de governança: verifica completude de
evidências, consistência das solicitações e — se um caminho de catálogo de
agentes for informado — reaproveita o validador do catálogo (audit_ai_agents).
Não conformidades viram itens de CAPA.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .agent_catalog import validate_catalog
from .evidence import EvidenceVault
from .ids import IDGenerator


@dataclass
class NonConformity:
    code: str
    description: str


@dataclass
class AuditReport:
    audit_id: str
    controls_checked: list[str] = field(default_factory=list)
    non_conformities: list[NonConformity] = field(default_factory=list)
    evidence_chain_valid: bool = True

    @property
    def passed(self) -> bool:
        return not self.non_conformities

    def summary(self) -> str:
        lines = [f"Auditoria {self.audit_id} — {'OK' if self.passed else 'NÃO CONFORME'}",
                 f"  controles verificados: {len(self.controls_checked)}",
                 f"  cadeia de evidências : {'íntegra' if self.evidence_chain_valid else 'ADULTERADA'}",
                 f"  não conformidades    : {len(self.non_conformities)}"]
        for nc in self.non_conformities:
            lines.append(f"  ✗ {nc.code}: {nc.description}")
        return "\n".join(lines)


class AuditEngine:
    def __init__(self, ids: IDGenerator, repository, evidence: EvidenceVault) -> None:
        self._ids = ids
        self._repo = repository
        self._evidence = evidence

    def run_monthly_audit(self, agent_catalog_path: str | None = None) -> AuditReport:
        report = AuditReport(audit_id=self._ids.create("WSS13-AUDIT"))
        ncs = report.non_conformities

        # Controle: integridade da cadeia de evidências (INVARIANT 10)
        report.controls_checked.append("evidence_chain_integrity")
        report.evidence_chain_valid = self._evidence.verify_chain()
        if not report.evidence_chain_valid:
            ncs.append(NonConformity("EVD-001", "Cadeia de evidências adulterada."))

        # Controle: toda solicitação tem avaliação de risco (INVARIANT 2)
        report.controls_checked.append("requests_have_risk_assessment")
        for req in self._repo.all_requests():
            if req.risk_assessment_id is None:
                ncs.append(NonConformity(
                    "REQ-002", f"Solicitação {req.request_id} sem avaliação de risco."))

        # Controle: todo incidente fechado tem causa raiz e ações (INVARIANT 9)
        report.controls_checked.append("closed_incidents_have_postmortem")
        for inc in self._repo.all_incidents():
            if inc.status.value == "CLOSED" and not inc.root_cause:
                ncs.append(NonConformity(
                    "INC-009", f"Incidente {inc.incident_id} fechado sem causa raiz."))

        # Controle: auditoria do catálogo de agentes (audit_ai_agents)
        if agent_catalog_path:
            report.controls_checked.append("ai_agents_catalog")
            catalog = validate_catalog(agent_catalog_path)
            for issue in catalog.issues:
                ncs.append(NonConformity(
                    "AI-004", f"Agente {issue.agent_id}: {'; '.join(issue.problems)}"))

        self._evidence.record(report.audit_id, "MONTHLY_AUDIT_COMPLETED", "COMPLIANCE_OWNER",
                             f"Auditoria concluída: {len(ncs)} não conformidades.")
        return report
