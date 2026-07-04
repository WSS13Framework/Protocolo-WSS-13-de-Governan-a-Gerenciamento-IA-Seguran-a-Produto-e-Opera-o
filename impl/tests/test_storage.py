import os
import tempfile
import unittest

from wss13_gos.orchestrator import GovernanceOrchestrator
from wss13_gos.storage import SQLiteRepository


class TestSQLiteRepository(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "test.db")
        self.repo = SQLiteRepository(self.path)

    def tearDown(self):
        self.repo.close()

    def test_roundtrip_request_and_evidence(self):
        gos = GovernanceOrchestrator(repository=self.repo)
        resp = gos.execute({
            "title": "persistir", "request_type": "DATA_PROCESSING",
            "involves_personal_data": True, "involves_external_client": True,
        })
        # relê a solicitação do SQLite
        loaded = self.repo.get_request(resp.request.request_id)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.request_id, resp.request.request_id)
        self.assertTrue(loaded.involves_personal_data)
        # a cadeia de evidências persiste e valida
        self.assertTrue(gos.evidence.verify_chain())
        self.assertGreaterEqual(len(self.repo.all_evidence()), 4)

    def test_persistence_across_connections(self):
        gos = GovernanceOrchestrator(repository=self.repo)
        resp = gos.execute({"title": "x"})
        rid = resp.request.request_id
        self.repo.close()
        # reabre em nova conexão
        repo2 = SQLiteRepository(self.path)
        self.assertIsNotNone(repo2.get_request(rid))
        repo2.close()


if __name__ == "__main__":
    unittest.main()
