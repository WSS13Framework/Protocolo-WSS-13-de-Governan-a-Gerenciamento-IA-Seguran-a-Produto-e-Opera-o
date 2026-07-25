"""MetricsEngine — painel executivo (seção 22)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .enums import ExecutionStatus, IncidentStatus, RiskLevel


@dataclass
class Dashboard:
    total_requests: int = 0
    requests_by_status: dict = field(default_factory=dict)
    requests_by_risk: dict = field(default_factory=dict)
    open_incidents: int = 0
    incidents_by_type: dict = field(default_factory=dict)
    high_and_critical_risks: int = 0
    evidence_records: int = 0
    evidence_chain_valid: bool = True

    def as_dict(self) -> dict:
        return asdict(self)


class MetricsEngine:
    def __init__(self, repository, evidence) -> None:
        self._repo = repository
        self._evidence = evidence

    def generate_executive_dashboard(self) -> Dashboard:
        requests = self._repo.all_requests()
        risks = self._repo.all_risks()
        incidents = self._repo.all_incidents()

        by_status: dict[str, int] = {}
        for r in requests:
            key = r.status.value if isinstance(r.status, ExecutionStatus) else str(r.status)
            by_status[key] = by_status.get(key, 0) + 1

        by_risk: dict[str, int] = {}
        for a in risks:
            key = a.risk_level.value if isinstance(a.risk_level, RiskLevel) else str(a.risk_level)
            by_risk[key] = by_risk.get(key, 0) + 1

        by_type: dict[str, int] = {}
        open_count = 0
        for inc in incidents:
            by_type[inc.incident_type] = by_type.get(inc.incident_type, 0) + 1
            if inc.status != IncidentStatus.CLOSED:
                open_count += 1

        high_crit = by_risk.get(RiskLevel.HIGH.value, 0) + by_risk.get(RiskLevel.CRITICAL.value, 0)

        return Dashboard(
            total_requests=len(requests),
            requests_by_status=by_status,
            requests_by_risk=by_risk,
            open_incidents=open_count,
            incidents_by_type=by_type,
            high_and_critical_risks=high_crit,
            evidence_records=len(self._repo.all_evidence()),
            evidence_chain_valid=self._evidence.verify_chain(),
        )
