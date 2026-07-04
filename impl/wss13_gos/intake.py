"""IntakeEngine e TriageEngine (seções 5 e 6)."""

from __future__ import annotations

from .enums import ExecutionStatus, RequestType
from .ids import IDGenerator
from .models import GovernanceRequest

APPROVED_CHANNELS = {"internal", "portal", "api", "email", "clickup", "jira"}


class UnauthorizedChannelError(ValueError):
    """Canal de entrada não autorizado (INTAKE rejeita)."""


class IntakeEngine:
    """MODULE IntakeEngine — porta de entrada oficial. Toda demanda gera um ID."""

    def __init__(self, ids: IDGenerator, repository) -> None:
        self._ids = ids
        self._repo = repository

    def register(self, event: dict) -> GovernanceRequest:
        channel = event.get("source_channel", "internal")
        if channel not in APPROVED_CHANNELS:
            raise UnauthorizedChannelError(f"Unauthorized input channel: {channel}")

        request = GovernanceRequest(
            request_id=self._ids.create("WSS13-GOV"),
            request_type=RequestType(event.get("request_type", RequestType.GENERAL_DEMAND.value)),
            title=event.get("title", "Untitled request"),
            description=event.get("description", ""),
            source_channel=channel,
            requester=event.get("requester", "system"),
            owner=event.get("owner", event.get("requester", "system")),
            department=event.get("department", "unassigned"),
            client_id=event.get("client_id"),
            product_id=event.get("product_id"),
            agent_id=event.get("agent_id"),
            vendor_id=event.get("vendor_id"),
            business_impact=int(event.get("business_impact", 1)),
            technical_complexity=int(event.get("technical_complexity", 1)),
            probability_override=event.get("probability_override"),
            status=ExecutionStatus.CREATED,
        )
        self._enrich_flags(request, event)
        self._repo.save_request(request)
        return request

    @staticmethod
    def _enrich_flags(request: GovernanceRequest, event: dict) -> None:
        """enrich_request_flags — deriva flags do evento de entrada."""
        request.involves_ai = bool(event.get("involves_ai", False))
        request.involves_personal_data = bool(event.get("involves_personal_data", False))
        request.involves_sensitive_data = bool(event.get("involves_sensitive_data", False))
        request.involves_security = bool(event.get("involves_security", False))
        request.involves_financial_impact = bool(event.get("involves_financial_impact", False))
        request.involves_external_client = bool(event.get("involves_external_client", False))
        request.involves_legal_contract = bool(event.get("involves_legal_contract", False))
        request.involves_api = bool(event.get("involves_api", False))
        request.involves_production_environment = bool(
            event.get("involves_production_environment", False)
        )
        # Tipos de solicitação de IA sempre marcam involves_ai.
        if request.request_type in (
            RequestType.AI_AGENT_CREATE,
            RequestType.AI_AGENT_UPDATE,
            RequestType.AI_AGENT_DISABLE,
        ):
            request.involves_ai = True


class TriageEngine:
    """MODULE TriageEngine — classifica em categorias e define prioridade."""

    def __init__(self, repository) -> None:
        self._repo = repository

    def classify(self, request: GovernanceRequest) -> dict:
        categories: list[str] = []
        if request.involves_ai:
            categories.append("AI_GOVERNANCE")
        if request.involves_personal_data or request.involves_sensitive_data:
            categories.append("DATA_PRIVACY")
        if request.involves_security:
            categories.append("SECURITY")
        if request.involves_production_environment:
            categories.append("DEVSECOPS")
        if request.involves_financial_impact:
            categories.append("FINANCE")
        if request.involves_legal_contract:
            categories.append("LEGAL")
        if request.request_type == RequestType.NEW_PRODUCT:
            categories.append("PRODUCT_GOVERNANCE")

        priority = self._calculate_priority(request)
        request.priority = priority
        request.status = ExecutionStatus.TRIAGED
        request.touch()
        self._repo.save_request(request)

        return {
            "request_id": request.request_id,
            "categories": categories,
            "priority": priority,
            "summary": "Request classified into: " + (", ".join(categories) or "GENERAL"),
        }

    @staticmethod
    def _calculate_priority(request: GovernanceRequest) -> str:
        score = request.business_impact + request.technical_complexity
        if request.involves_security or request.involves_sensitive_data:
            score += 3
        if score >= 8:
            return "CRITICAL"
        if score >= 6:
            return "HIGH"
        if score >= 4:
            return "MEDIUM"
        return "NORMAL"
