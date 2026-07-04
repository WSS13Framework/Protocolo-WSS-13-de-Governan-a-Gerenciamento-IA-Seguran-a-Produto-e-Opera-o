"""Validador do catálogo de agentes (audit_ai_agents, seção 19).

Lê o registro CSV dos 191 agentes e verifica cada linha contra as regras do
protocolo. Agentes com status PENDING_REGISTRATION são contados à parte (ainda
não aprovados); agentes REGISTERED/ACTIVE são validados integralmente.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field

from .enums import AIAutonomyLevel, RiskLevel

# Campos exigidos para um agente considerado registrado (INVARIANT 4).
REQUIRED_FIELDS = [
    "agent_name", "agent_category", "business_function", "product_context",
    "owner", "model_provider", "model_name", "prompt_version",
    "tools_allowed", "data_sources_allowed", "autonomy_level", "risk_level",
    "hallucination_threshold", "bias_threshold", "failure_threshold",
    "last_reviewed_at", "next_review_date",
]

PENDING = "PENDING_REGISTRATION"
_TRUE = {"true", "sim", "yes", "1"}
_HIGH_CRITICAL = {RiskLevel.HIGH.value, RiskLevel.CRITICAL.value}


@dataclass
class AgentIssue:
    agent_id: str
    problems: list[str] = field(default_factory=list)


@dataclass
class CatalogReport:
    total: int = 0
    pending: int = 0
    registered: int = 0
    valid: int = 0
    issues: list[AgentIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True se nenhum agente registrado tem problemas."""
        return not self.issues

    def summary(self) -> str:
        lines = [
            "Catálogo de Agentes — Relatório de Validação",
            f"  total          : {self.total}",
            f"  pendentes      : {self.pending}",
            f"  registrados    : {self.registered}",
            f"  válidos        : {self.valid}",
            f"  com problemas  : {len(self.issues)}",
        ]
        for issue in self.issues:
            lines.append(f"  ✗ {issue.agent_id}: {'; '.join(issue.problems)}")
        return "\n".join(lines)


def _is_true(value: str) -> bool:
    return (value or "").strip().lower() in _TRUE


def validate_row(row: dict) -> AgentIssue:
    agent_id = (row.get("agent_id") or "?").strip()
    problems: list[str] = []

    # Campos obrigatórios preenchidos
    for f in REQUIRED_FIELDS:
        if not (row.get(f) or "").strip():
            problems.append(f"campo obrigatório vazio: {f}")

    # Enums válidos
    autonomy = (row.get("autonomy_level") or "").strip()
    if autonomy and autonomy not in {e.value for e in AIAutonomyLevel}:
        problems.append(f"autonomy_level inválido: {autonomy}")

    risk = (row.get("risk_level") or "").strip()
    if risk and risk not in {e.value for e in RiskLevel}:
        problems.append(f"risk_level inválido: {risk}")

    # Regras para HIGH/CRITICAL (INVARIANT 5)
    if risk in _HIGH_CRITICAL:
        if not _is_true(row.get("has_kill_switch", "")):
            problems.append("HIGH/CRITICAL exige has_kill_switch")
        if not _is_true(row.get("requires_human_approval", "")):
            problems.append("HIGH/CRITICAL exige requires_human_approval")

    # LEVEL_5 exige kill switch + aprovação humana independentemente do risco
    if autonomy == AIAutonomyLevel.LEVEL_5_CRITICAL_AUTONOMOUS_ACTION.value:
        if not _is_true(row.get("has_kill_switch", "")):
            problems.append("LEVEL_5 exige has_kill_switch")
        if not _is_true(row.get("requires_human_approval", "")):
            problems.append("LEVEL_5 exige requires_human_approval")

    return AgentIssue(agent_id=agent_id, problems=problems)


def validate_catalog(path: str) -> CatalogReport:
    report = CatalogReport()
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            report.total += 1
            status = (row.get("status") or "").strip()
            if status == PENDING:
                report.pending += 1
                continue
            report.registered += 1
            issue = validate_row(row)
            if issue.problems:
                report.issues.append(issue)
            else:
                report.valid += 1
    return report
