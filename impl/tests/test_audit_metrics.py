import csv
import os
import tempfile
import unittest

from wss13_gos.enums import IncidentSeverity
from wss13_gos.orchestrator import GovernanceOrchestrator
from tests.test_agent_catalog import HEADER, _full_row, _write_csv


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.gos = GovernanceOrchestrator()

    def test_dashboard_counts(self):
        self.gos.execute({"title": "a"})
        self.gos.execute({"title": "b", "involves_sensitive_data": True,
                          "involves_production_environment": True, "involves_security": True,
                          "involves_external_client": True, "involves_ai": True,
                          "business_impact": 5, "technical_complexity": 5,
                          "probability_override": 5})
        self.gos.incidents.open_incident("AI", IncidentSeverity.SEV_2_HIGH, "x")
        dash = self.gos.metrics.generate_executive_dashboard()
        self.assertEqual(dash.total_requests, 2)
        self.assertEqual(dash.open_incidents, 1)
        self.assertEqual(dash.incidents_by_type.get("AI"), 1)
        self.assertTrue(dash.evidence_chain_valid)
        self.assertGreaterEqual(dash.high_and_critical_risks, 1)


class TestAudit(unittest.TestCase):
    def setUp(self):
        self.gos = GovernanceOrchestrator()

    def test_clean_audit_passes(self):
        self.gos.execute({"title": "a"})
        report = self.gos.audit.run_monthly_audit()
        self.assertTrue(report.passed)
        self.assertTrue(report.evidence_chain_valid)
        self.assertIn("requests_have_risk_assessment", report.controls_checked)

    def test_audit_flags_tampered_evidence(self):
        self.gos.execute({"title": "a"})
        # adultera evidência
        object.__setattr__(self.gos.repo.evidence[0], "description", "HACK")
        report = self.gos.audit.run_monthly_audit()
        self.assertFalse(report.passed)
        self.assertFalse(report.evidence_chain_valid)

    def test_audit_flags_bad_agent_in_catalog(self):
        # catálogo com um agente registrado inválido (HIGH sem kill switch)
        bad = _full_row(risk_level="HIGH", has_kill_switch="false",
                        requires_human_approval="false")
        path = _write_csv([bad])
        report = self.gos.audit.run_monthly_audit(agent_catalog_path=path)
        self.assertFalse(report.passed)
        self.assertTrue(any(nc.code == "AI-004" for nc in report.non_conformities))
        os.remove(path)


if __name__ == "__main__":
    unittest.main()
