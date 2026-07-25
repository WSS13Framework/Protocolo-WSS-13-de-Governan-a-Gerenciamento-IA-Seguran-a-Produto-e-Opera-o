import unittest

from wss13_gos.enums import IncidentSeverity, IncidentStatus
from wss13_gos.orchestrator import GovernanceOrchestrator


class TestIncidentEngine(unittest.TestCase):
    def setUp(self):
        self.gos = GovernanceOrchestrator()

    def test_open_incident_records_evidence(self):
        inc = self.gos.incidents.open_incident(
            "SECURITY", IncidentSeverity.SEV_2_HIGH, "brecha contida")
        self.assertEqual(inc.status, IncidentStatus.OPEN)
        events = [e.event_type for e in self.gos.repo.all_evidence()]
        self.assertIn("INCIDENT_OPENED", events)

    def test_data_breach_flags_regulatory_notification(self):
        inc = self.gos.incidents.open_incident(
            "PRIVACY", IncidentSeverity.SEV_1_CRITICAL, "vazamento",
            data_breach_suspected=True)
        self.assertTrue(inc.regulatory_notification_required)

    def test_kill_switch_opens_ai_incident(self):
        inc = self.gos.incidents.kill_switch("WSS13-AGENT-007", "alucinação grave", "CISO")
        self.assertTrue(inc.ai_failure_involved)
        events = [e.event_type for e in self.gos.repo.all_evidence()]
        self.assertIn("AI_AGENT_KILL_SWITCH_TRIGGERED", events)

    def test_handle_incident_closes_with_postmortem(self):
        inc = self.gos.incidents.open_incident(
            "OPERATIONAL", IncidentSeverity.SEV_3_MEDIUM, "degradação")
        closed = self.gos.incidents.handle_incident(
            inc.incident_id, "config errada", ["rollback", "novo teste"])
        self.assertEqual(closed.status, IncidentStatus.CLOSED)
        self.assertEqual(closed.root_cause, "config errada")
        self.assertIsNotNone(closed.resolved_at)


if __name__ == "__main__":
    unittest.main()
