"""RiskEngine — motor de risco corporativo (seção 7).

Pontua 8 dimensões (1..5) derivadas dos flags da solicitação, aplica a soma
ponderada do protocolo e classifica o nível de risco.

Nota de reconciliação: a soma ponderada bruta varia de ~12.9 a ~64.5, enquanto
as faixas de classify_risk_level (<=25/<=50/<=75/>75) operam numa escala 0..100.
Conforme documentado na matriz de riscos, o total é normalizado para 0..100 antes
da classificação, tornando as quatro faixas alcançáveis e consistentes.
"""

from __future__ import annotations

from .enums import RiskLevel, Role
from .ids import IDGenerator
from .models import GovernanceRequest, RiskAssessment

# Pesos oficiais (define a fórmula da seção 7).
WEIGHTS = {
    "ai": 1.4,
    "data": 1.5,
    "security": 1.5,
    "legal": 1.3,
    "financial": 1.1,
    "operational": 1.0,
    "reputation": 1.4,
    "client_impact": 1.2,
    "probability": 1.0,
    "impact": 1.5,
}

_TOTAL_WEIGHT = sum(WEIGHTS.values())
RAW_MIN = _TOTAL_WEIGHT * 1  # todas as dimensões = 1
RAW_MAX = _TOTAL_WEIGHT * 5  # todas as dimensões = 5


def _clamp(value: int, low: int = 1, high: int = 5) -> int:
    return max(low, min(high, value))


class RiskEngine:
    def __init__(self, ids: IDGenerator, repository) -> None:
        self._ids = ids
        self._repo = repository

    # --- pontuação por dimensão (score_*_risk) -------------------------------
    @staticmethod
    def score_ai_risk(r: GovernanceRequest) -> int:
        if not r.involves_ai:
            return 1
        return 4 if r.involves_production_environment else 3

    @staticmethod
    def score_data_risk(r: GovernanceRequest) -> int:
        if r.involves_sensitive_data:
            return 5
        if r.involves_personal_data:
            return 3
        return 1

    @staticmethod
    def score_security_risk(r: GovernanceRequest) -> int:
        if r.involves_security and r.involves_production_environment:
            return 5
        if r.involves_security or r.involves_production_environment:
            return 4
        return 1

    @staticmethod
    def score_legal_risk(r: GovernanceRequest) -> int:
        return 3 if r.involves_legal_contract else 1

    @staticmethod
    def score_financial_risk(r: GovernanceRequest) -> int:
        return 3 if r.involves_financial_impact else 1

    @staticmethod
    def score_operational_risk(r: GovernanceRequest) -> int:
        return _clamp(r.technical_complexity)

    @staticmethod
    def score_reputation_risk(r: GovernanceRequest) -> int:
        return 3 if r.involves_external_client else 1

    @staticmethod
    def score_client_impact(r: GovernanceRequest) -> int:
        return _clamp(r.business_impact) if r.involves_external_client else 1

    @staticmethod
    def calculate_probability(r: GovernanceRequest) -> int:
        if r.probability_override is not None:
            return _clamp(r.probability_override)
        return 2

    @staticmethod
    def classify_risk_level(total_score: float) -> RiskLevel:
        """Idêntico a classify_risk_level do pseudocódigo (escala 0..100)."""
        if total_score <= 25:
            return RiskLevel.LOW
        if total_score <= 50:
            return RiskLevel.MEDIUM
        if total_score <= 75:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    def assess(self, request: GovernanceRequest) -> RiskAssessment:
        ai = self.score_ai_risk(request)
        data = self.score_data_risk(request)
        security = self.score_security_risk(request)
        legal = self.score_legal_risk(request)
        financial = self.score_financial_risk(request)
        operational = self.score_operational_risk(request)
        reputation = self.score_reputation_risk(request)
        client_impact = self.score_client_impact(request)
        probability = self.calculate_probability(request)

        dims = [ai, data, security, legal, financial, operational, reputation, client_impact]
        impact = _clamp(round(sum(dims) / len(dims)))

        raw = (
            ai * WEIGHTS["ai"]
            + data * WEIGHTS["data"]
            + security * WEIGHTS["security"]
            + legal * WEIGHTS["legal"]
            + financial * WEIGHTS["financial"]
            + operational * WEIGHTS["operational"]
            + reputation * WEIGHTS["reputation"]
            + client_impact * WEIGHTS["client_impact"]
            + probability * WEIGHTS["probability"]
            + impact * WEIGHTS["impact"]
        )
        normalized = round((raw - RAW_MIN) / (RAW_MAX - RAW_MIN) * 100, 2)
        level = self.classify_risk_level(normalized)

        assessment = RiskAssessment(
            risk_id=self._ids.create("WSS13-RISK"),
            request_id=request.request_id,
            ai_risk_score=ai,
            data_risk_score=data,
            security_risk_score=security,
            legal_risk_score=legal,
            financial_risk_score=financial,
            operational_risk_score=operational,
            reputation_risk_score=reputation,
            client_impact_score=client_impact,
            probability_score=probability,
            impact_score=impact,
            raw_score=round(raw, 2),
            total_score=normalized,
            risk_level=level,
            required_controls=self._define_controls(request, level),
            required_approvers=self._define_required_approvers(request, level),
            requires_dpia=self._requires_dpia(request),
            requires_ai_review=request.involves_ai and level in (RiskLevel.HIGH, RiskLevel.CRITICAL),
            requires_security_review=(
                request.involves_security or request.involves_production_environment
            ),
            requires_legal_review=request.involves_legal_contract or level == RiskLevel.CRITICAL,
            requires_founder_board=level == RiskLevel.CRITICAL,
        )
        self._repo.save_risk(assessment)
        request.risk_assessment_id = assessment.risk_id
        return assessment

    @staticmethod
    def _requires_dpia(r: GovernanceRequest) -> bool:
        # DPIA disparada por dado pessoal/sensível (independe do nível).
        return r.involves_personal_data or r.involves_sensitive_data

    @staticmethod
    def _define_controls(r: GovernanceRequest, level: RiskLevel) -> list[str]:
        controls = ["registro", "dono", "evidencia", "avaliacao_de_risco"]
        if r.involves_production_environment:
            controls += ["rollback_plan", "code_review", "tests", "deploy_evidence"]
        if r.involves_ai and level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            controls += ["kill_switch", "human_review", "red_team"]
        if r.involves_personal_data or r.involves_sensitive_data:
            controls += ["base_legal", "retencao", "controle_de_acesso", "criptografia"]
        return controls

    @staticmethod
    def _define_required_approvers(r: GovernanceRequest, level: RiskLevel) -> list[Role]:
        """FUNCTION define_required_approvers (seção 8) — ordem e deduplicação preservadas."""
        approvers: list[Role] = [Role.OWNER]
        if r.involves_ai:
            approvers.append(Role.AI_OFFICER)
        if r.involves_personal_data or r.involves_sensitive_data:
            approvers.append(Role.DPO)
        if r.involves_security or r.involves_production_environment:
            approvers.append(Role.CTO)
            approvers.append(Role.CISO)
        if r.involves_legal_contract:
            approvers.append(Role.LEGAL)
        if r.involves_financial_impact:
            approvers.append(Role.CFO)
        if level == RiskLevel.HIGH:
            approvers.append(Role.CEO)
        if level == RiskLevel.CRITICAL:
            approvers.append(Role.FOUNDER_BOARD)
        # unique(approvers) preservando a ordem
        seen: set[Role] = set()
        unique: list[Role] = []
        for a in approvers:
            if a not in seen:
                seen.add(a)
                unique.append(a)
        return unique
