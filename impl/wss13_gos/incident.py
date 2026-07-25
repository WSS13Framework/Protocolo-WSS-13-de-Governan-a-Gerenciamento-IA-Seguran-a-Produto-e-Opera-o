"""IncidentEngine — gestão de incidentes (seção 16) e kill switch (seção 9)."""

from __future__ import annotations

from datetime import datetime, timezone

from .enums import IncidentSeverity, IncidentStatus
from .evidence import EvidenceVault
from .ids import IDGenerator
from .models import Incident

_HIGH_SEVERITIES = {IncidentSeverity.SEV_2_HIGH, IncidentSeverity.SEV_1_CRITICAL}


class IncidentEngine:
    def __init__(self, ids: IDGenerator, repository, evidence: EvidenceVault) -> None:
        self._ids = ids
        self._repo = repository
        self._evidence = evidence

    def open_incident(self, incident_type: str, severity: IncidentSeverity,
                      description: str, *, title: str | None = None,
                      commander: str = "SYSTEM", **kwargs) -> Incident:
        incident = Incident(
            incident_id=self._ids.create("WSS13-INC"),
            title=title or description[:80] or incident_type,
            severity=severity,
            incident_type=incident_type,
            description=description,
            commander=commander,
            data_breach_suspected=bool(kwargs.get("data_breach_suspected", False)),
            ai_failure_involved=bool(kwargs.get("ai_failure_involved", False)),
            affected_systems=list(kwargs.get("affected_systems", [])),
            affected_customers=list(kwargs.get("affected_customers", [])),
        )
        # Suspeita de violação de dados pessoais dispara avaliação de notificação regulatória.
        incident.regulatory_notification_required = incident.data_breach_suspected
        self._repo.save_incident(incident)
        self._evidence.record(incident.incident_id, "INCIDENT_OPENED", commander, description)
        return incident

    def kill_switch(self, agent_id: str, reason: str, actor: str) -> Incident:
        """Aciona o kill switch de um agente e abre incidente AI (seção 9)."""
        incident = self.open_incident(
            incident_type="AI",
            severity=IncidentSeverity.SEV_2_HIGH,
            description=f"Agent disabled by kill switch: {agent_id}. Reason: {reason}",
            title=f"Kill switch: {agent_id}",
            commander=actor,
            ai_failure_involved=True,
        )
        self._evidence.record(f"EMERGENCY-{agent_id}", "AI_AGENT_KILL_SWITCH_TRIGGERED",
                             actor, reason)
        return incident

    def handle_incident(self, incident_id: str, root_cause: str,
                        corrective_actions: list[str], *,
                        now: datetime | None = None) -> Incident:
        incident = self._repo.get_incident(incident_id)
        if incident is None:
            raise KeyError(incident_id)
        incident.root_cause = root_cause
        incident.corrective_actions = list(corrective_actions)
        incident.status = IncidentStatus.CLOSED
        incident.resolved_at = now or datetime.now(timezone.utc)
        self._repo.save_incident(incident)
        self._evidence.record(incident_id, "INCIDENT_CLOSED", incident.commander,
                             "Incident closed with postmortem.")
        return incident
