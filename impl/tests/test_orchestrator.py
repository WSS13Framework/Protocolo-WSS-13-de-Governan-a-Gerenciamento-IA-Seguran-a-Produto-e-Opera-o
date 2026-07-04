import unittest

from wss13_gos.approval import auto_approve
from wss13_gos.enums import ApprovalStatus, ExecutionStatus, RiskLevel, Role
from wss13_gos.intake import UnauthorizedChannelError
from wss13_gos.models import ApprovalDecision
from wss13_gos.orchestrator import GovernanceOrchestrator


class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.gos = GovernanceOrchestrator()

    def test_happy_path_low_risk_closes(self):
        resp = self.gos.execute({"title": "trivial", "request_type": "PRODUCT_CHANGE"})
        self.assertEqual(resp.status, "SUCCESS")
        self.assertEqual(resp.request.status, ExecutionStatus.CLOSED)
        self.assertEqual(resp.risk_assessment.risk_level, RiskLevel.LOW)

    def test_rejection_stops_pipeline(self):
        def reject(approver, request, assessment):
            if approver == Role.CISO:
                return ApprovalDecision(approver, ApprovalStatus.REJECTED, "no")
            return auto_approve(approver, request, assessment)

        resp = self.gos.execute(
            {"title": "deploy", "request_type": "SECURITY_CHANGE",
             "involves_security": True, "involves_production_environment": True},
            resolver=reject,
        )
        self.assertEqual(resp.status, "REJECTED")
        self.assertEqual(resp.request.status, ExecutionStatus.REJECTED)

    def test_needs_review_becomes_pending(self):
        def review(approver, request, assessment):
            return ApprovalDecision(approver, ApprovalStatus.NEEDS_REVIEW, "revisar")

        resp = self.gos.execute({"title": "x", "request_type": "GENERAL_DEMAND"},
                                resolver=review)
        self.assertEqual(resp.status, "PENDING_APPROVAL")

    def test_unauthorized_channel_raises(self):
        with self.assertRaises(UnauthorizedChannelError):
            self.gos.execute({"title": "x", "source_channel": "carrier-pigeon"})

    def test_evidence_generated_for_each_step(self):
        resp = self.gos.execute({"title": "trivial"})
        events = [e.event_type for e in self.gos.repo.all_evidence()
                  if e.request_id == resp.request.request_id]
        for expected in ["REQUEST_CREATED", "REQUEST_TRIAGED", "RISK_ASSESSED",
                         "APPROVAL_DECISION", "REQUEST_CLOSED"]:
            self.assertIn(expected, events)
        self.assertTrue(self.gos.evidence.verify_chain())


if __name__ == "__main__":
    unittest.main()
