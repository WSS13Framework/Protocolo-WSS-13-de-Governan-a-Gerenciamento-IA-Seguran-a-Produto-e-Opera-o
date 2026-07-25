import unittest

from wss13_gos.enums import RiskLevel, Role
from wss13_gos.ids import IDGenerator
from wss13_gos.intake import IntakeEngine
from wss13_gos.risk import RAW_MAX, RAW_MIN, RiskEngine
from wss13_gos.storage import InMemoryRepository


def build_request(**event):
    repo = InMemoryRepository()
    ids = IDGenerator()
    intake = IntakeEngine(ids, repo)
    return intake.register(event), repo, ids


class TestRiskScoring(unittest.TestCase):
    def test_classify_thresholds(self):
        classify = RiskEngine.classify_risk_level
        self.assertEqual(classify(25), RiskLevel.LOW)
        self.assertEqual(classify(25.1), RiskLevel.MEDIUM)
        self.assertEqual(classify(50), RiskLevel.MEDIUM)
        self.assertEqual(classify(75), RiskLevel.HIGH)
        self.assertEqual(classify(75.1), RiskLevel.CRITICAL)
        self.assertEqual(classify(100), RiskLevel.CRITICAL)

    def test_normalization_bounds(self):
        # menor risco possível -> 0 ; maior -> 100
        req_low, repo, ids = build_request(title="trivial")
        engine = RiskEngine(ids, repo)
        a_low = engine.assess(req_low)
        self.assertGreaterEqual(a_low.total_score, 0)
        self.assertEqual(a_low.risk_level, RiskLevel.LOW)

        req_hi, repo2, ids2 = build_request(
            title="tudo alto",
            involves_ai=True,
            involves_sensitive_data=True,
            involves_security=True,
            involves_production_environment=True,
            involves_legal_contract=True,
            involves_financial_impact=True,
            involves_external_client=True,
            business_impact=5,
            technical_complexity=5,
            probability_override=5,
        )
        a_hi = RiskEngine(ids2, repo2).assess(req_hi)
        self.assertEqual(a_hi.risk_level, RiskLevel.CRITICAL)
        self.assertLessEqual(a_hi.total_score, 100)

    def test_raw_bounds_constants(self):
        # 10 dimensões, pesos somam 12.9 -> min 12.9, max 64.5
        self.assertAlmostEqual(RAW_MIN, 12.9, places=2)
        self.assertAlmostEqual(RAW_MAX, 64.5, places=2)

    def test_sensitive_data_requires_dpo_and_dpia(self):
        req, repo, ids = build_request(
            title="dado sensível", involves_sensitive_data=True
        )
        a = RiskEngine(ids, repo).assess(req)
        self.assertIn(Role.DPO, a.required_approvers)
        self.assertTrue(a.requires_dpia)

    def test_production_security_adds_cto_ciso(self):
        req, repo, ids = build_request(
            title="deploy", involves_security=True, involves_production_environment=True
        )
        a = RiskEngine(ids, repo).assess(req)
        self.assertIn(Role.CTO, a.required_approvers)
        self.assertIn(Role.CISO, a.required_approvers)

    def test_approvers_are_unique_and_ordered(self):
        req, repo, ids = build_request(
            title="ai+prod", involves_ai=True, involves_production_environment=True
        )
        a = RiskEngine(ids, repo).assess(req)
        self.assertEqual(len(a.required_approvers), len(set(a.required_approvers)))
        self.assertEqual(a.required_approvers[0], Role.OWNER)


if __name__ == "__main__":
    unittest.main()
