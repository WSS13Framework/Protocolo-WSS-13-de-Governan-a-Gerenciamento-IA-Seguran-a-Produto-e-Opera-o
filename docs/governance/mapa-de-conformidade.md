# Mapa de Conformidade — WSS+13 SGI-AI OS

> Vincula os controles do protocolo (`GOVERNANCE_STANDARDS`, Apêndice A) às normas visadas.
> Classificação: `INTERNAL_PROPRIETARY`.

Este mapa mostra **onde cada norma é atendida** dentro do protocolo, servindo de base para
auditorias e para o `quarterly_strategic_review`.

---

## 1. Cobertura por norma

| Norma | Escopo | Onde é atendida no protocolo |
|---|---|---|
| **ISO 9001** | Qualidade | Melhoria contínua (§20), auditoria (§19), CAPA, QA na execução (§4) |
| **ISO 27001** | Segurança da informação | SecurityEngine (§11), DevSecOps, controle de acesso, cripto, incidentes (§16) |
| **ISO 27701** | Privacidade (PIMS) | DataGovernanceEngine (§10), DPIA, direitos de titular, retenção |
| **ISO 42001** | Gestão de IA | AIGovernanceEngine (§9), catálogo de agentes, autonomia, red team, kill switch |
| **SOC 2** | Trust Services Criteria | Evidências (§18), auditoria (§19), continuidade (§17), segurança (§11) |
| **NIST AI RMF** | Risco de IA | RiskEngine (§7) + suíte de avaliação de agentes (§9) |
| **NIST CSF** | Cibersegurança | SecurityEngine, monitoramento, resposta a incidentes, recuperação |
| **OWASP ASVS / Top 10** | Segurança de aplicação | Checks de DevSecOps (SAST, deps, segredos, API security) |
| **OWASP LLM Top 10** | Segurança de LLM | Testes de prompt injection, vazamento, abuso de ferramentas (§9) |
| **LGPD** | Proteção de dados (BR) | Base legal, finalidade, DPIA/RIPD, direitos do titular, DPO |
| **GDPR (readiness)** | Proteção de dados (EU) | idem LGPD + transferência internacional, DPA |
| **EU AI Act (readiness)** | Regulação de IA (EU) | Classificação de risco de IA, transparência, supervisão humana, logs |

---

## 2. Mapa Trust Services Criteria (SOC 2)

| Critério | Controle do protocolo |
|---|---|
| **Security** | SecurityEngine (§11), MFA, RBAC, cripto, segregação de ambientes |
| **Availability** | ContinuityEngine (§17), RTO/RPO, backup, DR test, monitoramento |
| **Processing Integrity** | QA na execução, validação pré-execução, reconciliação financeira (§14) |
| **Confidentiality** | Classificação de dados, cofre de segredos, controle de acesso |
| **Privacy** | DataGovernanceEngine (§10), DPIA, retenção, direitos do titular |

---

## 3. Ciclo de conformidade contínua

| Frequência | Job | Ação |
|---|---|---|
| Diária | `daily_governance_check` | Incidentes críticos, aprovações vencidas, alertas de segurança |
| Semanal | `weekly_operational_review` | Relatórios de produto, IA, segurança, riscos abertos |
| Mensal | `monthly_compliance_review` | `run_monthly_audit`, revisão de acessos, fornecedores, retenção |
| Trimestral | `quarterly_strategic_review` | Prontidão ISO 9001/27001/42001, SOC 2, GDPR, AI Act |

---

## 4. Trilha de evidências

Cada controle produz evidência imutável e com hash (`INVARIANT 10`) no
[Cofre de Evidências](../WSS13-SGI-AI-PSEUDOCODE-001.md#18-cofre-de-evidências).
Os tipos de evidência (`ENUM EvidenceType`) cobrem desde `RISK_ASSESSMENT` e `AI_EVALUATION`
até `DEPLOY_LOG`, `INCIDENT_REPORT` e `AUDIT_RECORD` — dando rastreabilidade ponta a ponta para
qualquer auditor.

---

## 5. Situação de prontidão (a manter atualizada)

| Norma | Prontidão | Próximo passo |
|---|---|---|
| ISO 9001 | 🟡 Estruturado | Formalizar manual da qualidade e indicadores |
| ISO 27001 | 🟡 Estruturado | SoA (Declaração de Aplicabilidade) + Anexo A |
| ISO 27701 | 🟡 Estruturado | Inventário de tratamentos + RIPD por tratamento |
| ISO 42001 | 🟡 Estruturado | Catalogar os 191 agentes (Fase 3) |
| SOC 2 | 🟡 Estruturado | Período de observação de controles |
| LGPD / GDPR | 🟡 Estruturado | Registro de operações de tratamento (RoPA) |
| EU AI Act | 🟢 Readiness | Classificação de risco por sistema de IA |

> 🟢 Pronto · 🟡 Estruturado (base pronta, falta operar/evidenciar) · 🔴 Gap.
