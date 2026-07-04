import unittest

from wss13_gos.evidence import EvidenceVault
from wss13_gos.ids import IDGenerator
from wss13_gos.storage import InMemoryRepository


class TestEvidenceVault(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.vault = EvidenceVault(IDGenerator(), self.repo)

    def test_records_are_hashed_and_chained(self):
        e1 = self.vault.record("WSS13-GOV-2026-0001", "REQUEST_CREATED", "ana", "criado")
        e2 = self.vault.record("WSS13-GOV-2026-0001", "RISK_ASSESSED", "SYSTEM", "risco")
        self.assertNotEqual(e1.content_hash, e2.content_hash)
        self.assertTrue(self.vault.verify_chain())

    def test_tampering_is_detected(self):
        self.vault.record("WSS13-GOV-2026-0001", "REQUEST_CREATED", "ana", "criado")
        self.vault.record("WSS13-GOV-2026-0001", "RISK_ASSESSED", "SYSTEM", "risco")
        # adultera a descrição do primeiro registro (frozen dataclass -> troca no repo)
        tampered = self.repo.evidence[0]
        object.__setattr__(tampered, "description", "ADULTERADO")
        self.assertFalse(self.vault.verify_chain())

    def test_evidence_ids_are_sequential(self):
        e1 = self.vault.record("r", "A", "x", "d")
        e2 = self.vault.record("r", "B", "x", "d")
        self.assertTrue(e1.evidence_id.startswith("WSS13-EVD-"))
        self.assertNotEqual(e1.evidence_id, e2.evidence_id)


if __name__ == "__main__":
    unittest.main()
