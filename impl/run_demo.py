#!/usr/bin/env python3
"""Demonstração do pipeline WSS13_GOS com três solicitações de risco crescente.

Uso: python3 impl/run_demo.py
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime

from wss13_gos.orchestrator import GovernanceOrchestrator


def _default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if hasattr(o, "value"):
        return o.value
    raise TypeError


SCENARIOS = [
    {
        "title": "Atualizar texto da landing page",
        "request_type": "PRODUCT_CHANGE",
        "requester": "ana",
        "business_impact": 1,
        "technical_complexity": 1,
    },
    {
        "title": "Novo agente de diagnóstico com dado pessoal",
        "request_type": "AI_AGENT_CREATE",
        "requester": "bruno",
        "involves_personal_data": True,
        "involves_external_client": True,
        "business_impact": 3,
        "technical_complexity": 3,
    },
    {
        "title": "Agente autônomo em produção acessando dado sensível",
        "request_type": "AI_AGENT_CREATE",
        "requester": "carla",
        "involves_sensitive_data": True,
        "involves_security": True,
        "involves_production_environment": True,
        "involves_external_client": True,
        "business_impact": 5,
        "technical_complexity": 5,
        "probability_override": 4,
    },
]


def main() -> None:
    gos = GovernanceOrchestrator()
    for scenario in SCENARIOS:
        resp = gos.execute(scenario)
        ra = resp.risk_assessment
        print("=" * 72)
        print(f"{resp.request.request_id}  |  {scenario['title']}")
        print(f"  status        : {resp.status}")
        print(f"  risco         : {ra.risk_level.value}  (score {ra.total_score} / raw {ra.raw_score})")
        print(f"  aprovadores   : {', '.join(r.value for r in ra.required_approvers)}")
        print(f"  DPIA          : {ra.requires_dpia}   red-team/IA: {ra.requires_ai_review}")
    print("=" * 72)
    print(f"cadeia de evidências íntegra: {gos.evidence.verify_chain()}")
    print(f"total de evidências        : {len(gos.repo.all_evidence())}")


if __name__ == "__main__":
    main()
