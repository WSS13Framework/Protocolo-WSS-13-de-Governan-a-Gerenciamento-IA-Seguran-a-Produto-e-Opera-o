# WSS13_GOS — Implementação de Referência (Fase 1)

Implementação **executável** dos motores centrais do protocolo mestre
([`WSS13-SGI-AI-PSEUDOCODE-001`](../docs/WSS13-SGI-AI-PSEUDOCODE-001.md)), construída
**apenas com a biblioteca padrão do Python 3.11+** — sem dependências externas.

> Esta é a base do software proprietário de governança da WSS+13. Cobre o caminho
> Intake → Triage → Risk → Approval → Evidence (seções 4–8 e 18). Execução/QA/Release,
> IA, dados, incidentes e demais motores serão adicionados nas próximas fases.

## Estrutura

```
impl/
├── wss13_gos/
│   ├── enums.py          # RequestType, RiskLevel, ApprovalStatus, ExecutionStatus, Role…
│   ├── models.py         # GovernanceRequest, RiskAssessment, EvidenceRecord, ApprovalFlow…
│   ├── ids.py            # IDGenerator (PREFIX-YYYY-NNNN)
│   ├── evidence.py       # EvidenceVault — hash encadeado, imutável (INVARIANT 10)
│   ├── intake.py         # IntakeEngine + TriageEngine (seções 5–6)
│   ├── risk.py           # RiskEngine — pontuação ponderada e classificação (seção 7)
│   ├── approval.py       # ApprovalEngine — alçadas/RACI (seção 8)
│   ├── orchestrator.py   # WSS13_GOS_MAIN — pipeline (seção 4)
│   ├── storage.py        # InMemoryRepository + SQLiteRepository
│   ├── api.py            # API HTTP mínima (stdlib)
│   ├── agent_catalog.py  # validador do catálogo dos 191 agentes (audit_ai_agents)
│   └── validate_catalog.py # CLI do validador
├── tests/                # 28 testes (unittest)
└── run_demo.py           # demonstração ponta a ponta
```

## Como rodar

```bash
cd impl

# Testes (nenhuma dependência necessária)
python3 -m unittest discover -s tests -v

# Demonstração ponta a ponta (3 cenários de risco crescente)
python3 run_demo.py

# API HTTP local
python3 -m wss13_gos.api        # http://127.0.0.1:8013

# Validar o catálogo dos 191 agentes
python3 -m wss13_gos.validate_catalog
```

### Exemplo de uso da API

```bash
curl -s -X POST http://127.0.0.1:8013/requests \
  -H 'Content-Type: application/json' \
  -d '{"title":"Novo agente","request_type":"AI_AGENT_CREATE",
       "involves_sensitive_data":true,"involves_production_environment":true}'
# -> {"status":"SUCCESS","risk_level":"HIGH","required_approvers":["OWNER","AI_OFFICER","DPO","CTO","CISO","CEO"], ...}

curl -s http://127.0.0.1:8013/evidence/verify   # {"chain_valid": true}
```

## Decisões de projeto

- **Reconciliação da escala de risco.** A soma ponderada bruta da seção 7 varia de `12.9`
  a `64.5`, mas as faixas de `classify_risk_level` (`≤25/≤50/≤75/>75`) operam em `0–100`.
  A implementação normaliza o total para `0–100` antes de classificar — tornando as quatro
  faixas alcançáveis e consistentes, conforme documentado na
  [matriz de riscos](../docs/governance/matriz-de-riscos.md).
- **Evidência como cadeia de hash.** Cada registro encadeia o hash do anterior (SHA-256);
  `verify_chain()` detecta qualquer adulteração, satisfazendo o `INVARIANT 10`.
- **Resolvedor de decisão plugável.** `ApprovalEngine.route` recebe um `DecisionResolver`,
  permitindo simulação (auto-aprovação), integração com humanos ou fluxos externos.
- **Sem dependências.** Facilita auditoria, portabilidade e execução em CI restrita.

## Cobertura de invariantes (testes)

| Invariante | Teste |
|---|---|
| 1 — campos obrigatórios | `test_invariant1_request_has_mandatory_fields` |
| 2 — sem execução sem avaliação de risco | `test_invariant2_no_execution_without_risk_assessment` |
| 5 — IA HIGH/CRITICAL exige revisão humana + kill switch | `test_invariant5_high_risk_ai_requires_human_review_controls` |
| 6 — dado pessoal exige controles | `test_invariant6_personal_data_requires_controls` |
| 10 — evidência imutável e com hash | `test_invariant10_immutable_hashed_evidence` |
