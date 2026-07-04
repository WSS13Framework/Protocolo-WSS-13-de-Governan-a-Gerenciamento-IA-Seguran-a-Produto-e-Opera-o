"""Testes que verificam invariantes do protocolo (Apêndice D)."""

import unittest

from wss13_gos.enums import RiskLevel
from wss13_gos.orchestrator import GovernanceOrchestrator


class TestInvariants(unittest.TestCase):
    def setUp(self):
        self.gos = GovernanceOrchestrator()

    def test_invariant1_request_has_mandatory_fields(self):
        resp = self.gos.execute({"title": "x", "request_type": "GENERAL_DEMAND"})
        r = resp.request
        self.assertTrue(r.request_id)
        self.assertTrue(r.owner)
        self.assertIsNotNone(r.request_type)
        self.assertIsNotNone(resp.risk_assessment.risk_level)

    def test_invariant2_no_execution_without_risk_assessment(self):
        # o pipeline sempre produz risk_assessment antes de aprovar/fechar
        resp = self.gos.execute({"title": "x"})
        self.assertIsNotNone(resp.risk_assessment)
        self.assertIsNotNone(resp.request.risk_assessment_id)

    def test_invariant5_high_risk_ai_requires_human_review_controls(self):
        resp = self.gos.execute({
            "title": "agente crítico",
            "request_type": "AI_AGENT_CREATE",
            "involves_ai": True,
            "involves_sensitive_data": True,
            "involves_security": True,
            "involves_production_environment": True,
            "involves_external_client": True,
            "business_impact": 5,
            "technical_complexity": 5,
            "probability_override": 5,
        })
        ra = resp.risk_assessment
        self.assertIn(ra.risk_level, (RiskLevel.HIGH, RiskLevel.CRITICAL))
        self.assertIn("kill_switch", ra.required_controls)
        self.assertIn("human_review", ra.required_controls)

    def test_invariant6_personal_data_requires_controls(self):
        resp = self.gos.execute({"title": "dado", "involves_personal_data": True})
        ra = resp.risk_assessment
        for c in ("base_legal", "retencao", "controle_de_acesso", "criptografia"):
            self.assertIn(c, ra.required_controls)

    def test_invariant10_immutable_hashed_evidence(self):
        self.gos.execute({"title": "x"})
        self.assertTrue(self.gos.evidence.verify_chain())
        self.assertTrue(all(e.content_hash for e in self.gos.repo.all_evidence()))


if __name__ == "__main__":
    unittest.main()
