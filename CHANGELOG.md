# Changelog — WSS+13 SGI-AI OS

Controle de versão do ativo de governança (`ASSET_PROTECTION_RULE` exige `version_control`).
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versionamento semântico do protocolo.

## [Não lançado]

### Adicionado — Implementação de referência WSS13_GOS (Fase 1)
- Pacote `impl/wss13_gos/` (Python 3.11, apenas stdlib) com os motores Intake, Triage,
  Risk, Approval e o cofre de evidências (EvidenceVault), orquestrados por um pipeline
  equivalente a `WSS13_GOS_MAIN`.
- Persistência dupla: `InMemoryRepository` e `SQLiteRepository`.
- API HTTP mínima (`wss13_gos/api.py`) e demonstração ponta a ponta (`run_demo.py`).
- Suíte de 21 testes cobrindo pontuação de risco, alçadas, cadeia de evidências e invariantes.
- Workflow de CI (`.github/workflows/ci.yml`) rodando testes + demo. `.gitignore` adicionado.

### Adicionado — Camada de governança operacional (Fase 0)
- Matriz de riscos (`docs/governance/matriz-de-riscos.md`).
- Matriz de aprovação e alçadas / RACI (`docs/governance/matriz-de-aprovacao.md`).
- Catálogo dos 191 agentes de IA (`docs/governance/catalogo-de-agentes-ia.md`).
- Classificação de dados, LGPD e GDPR (`docs/governance/classificacao-de-dados-lgpd.md`).
- Mapa de conformidade ISO/SOC 2/NIST/LGPD/GDPR/EU AI Act (`docs/governance/mapa-de-conformidade.md`).
- Registros operacionais: catálogo de agentes, riscos, fornecedores e ativos de dados (`registers/`).
- Modelos: solicitação de governança, avaliação de risco, DPIA e postmortem (`templates/`).
- README atualizado com estrutura e roadmap; este CHANGELOG.

## [1.0.0] — 2026-07-04

### Adicionado
- Documento mestre `WSS13-SGI-AI-PSEUDOCODE-001` v1.0.0: pseudocódigo do Sistema de Governança
  Integrado com 24 seções e 4 apêndices (constantes, enumerações, entidades e invariantes).
- README inicial e identificação do ativo.
