import csv
import os
import tempfile
import unittest

from wss13_gos.agent_catalog import validate_catalog, validate_row

HEADER = [
    "agent_id", "agent_number", "agent_name", "agent_category", "business_function",
    "product_context", "owner", "model_provider", "model_name", "prompt_version",
    "tools_allowed", "data_sources_allowed", "autonomy_level", "risk_level",
    "has_kill_switch", "requires_human_approval", "hallucination_threshold",
    "bias_threshold", "failure_threshold", "status", "last_reviewed_at", "next_review_date",
]


def _full_row(**overrides):
    base = {k: "x" for k in HEADER}
    base.update({
        "agent_id": "WSS13-AGENT-001", "agent_number": "1",
        "autonomy_level": "LEVEL_2_RECOMMENDATION", "risk_level": "MEDIUM",
        "has_kill_switch": "true", "requires_human_approval": "false",
        "status": "REGISTERED",
    })
    base.update(overrides)
    return base


def _write_csv(rows):
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


class TestAgentCatalog(unittest.TestCase):
    def test_pending_rows_are_not_validated(self):
        row = {k: "" for k in HEADER}
        row.update({"agent_id": "WSS13-AGENT-001", "status": "PENDING_REGISTRATION"})
        path = _write_csv([row])
        report = validate_catalog(path)
        self.assertEqual(report.pending, 1)
        self.assertEqual(report.registered, 0)
        self.assertTrue(report.ok)

    def test_complete_registered_row_is_valid(self):
        path = _write_csv([_full_row()])
        report = validate_catalog(path)
        self.assertEqual(report.registered, 1)
        self.assertEqual(report.valid, 1)
        self.assertTrue(report.ok)

    def test_missing_field_flagged(self):
        issue = validate_row(_full_row(owner=""))
        self.assertTrue(any("owner" in p for p in issue.problems))

    def test_high_risk_requires_kill_switch_and_human_approval(self):
        issue = validate_row(_full_row(
            risk_level="CRITICAL", has_kill_switch="false", requires_human_approval="false"
        ))
        self.assertTrue(any("has_kill_switch" in p for p in issue.problems))
        self.assertTrue(any("requires_human_approval" in p for p in issue.problems))

    def test_level5_requires_controls(self):
        issue = validate_row(_full_row(
            autonomy_level="LEVEL_5_CRITICAL_AUTONOMOUS_ACTION",
            risk_level="LOW", has_kill_switch="false", requires_human_approval="false",
        ))
        self.assertTrue(any("LEVEL_5" in p for p in issue.problems))

    def test_invalid_enum_flagged(self):
        issue = validate_row(_full_row(autonomy_level="LEVEL_9", risk_level="EXTREME"))
        self.assertTrue(any("autonomy_level inválido" in p for p in issue.problems))
        self.assertTrue(any("risk_level inválido" in p for p in issue.problems))


class TestRealSkeleton(unittest.TestCase):
    """O esqueleto dos 191 agentes deve ser lido sem erro e contar 191 pendentes."""

    def test_skeleton_has_191_pending(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "registers", "catalogo-agentes.csv"
        )
        if not os.path.exists(path):
            self.skipTest("catálogo não encontrado")
        report = validate_catalog(path)
        self.assertEqual(report.total, 191)
        self.assertEqual(report.pending, 191)
        self.assertTrue(report.ok)  # nada registrado ainda -> sem problemas


if __name__ == "__main__":
    unittest.main()
