# Matriz de Aprovação e Alçadas (RACI) — WSS+13 SGI-AI OS

> Derivada de `FUNCTION define_required_approvers` (seção 8) e do `MODULE ApprovalEngine`.
> Classificação: `INTERNAL_PROPRIETARY`.

Define **quem aprova o quê**, em função das características da solicitação e do nível de risco.
Nenhuma solicitação avança sem passar por **todos** os aprovadores exigidos (`INVARIANT 3`).

---

## 1. Papéis de governança

| Sigla | Papel | Domínio |
|---|---|---|
| OWNER | Dono da solicitação | Responsável primário |
| AI_OFFICER | Responsável de IA | Governança de agentes e modelos |
| DPO | Encarregado de dados | LGPD/GDPR, privacidade |
| CTO | Diretor de tecnologia | Engenharia, produção |
| CISO | Diretor de segurança | Segurança da informação |
| LEGAL | Responsável jurídico | Contratos, regulatório |
| CFO | Diretor financeiro | Finanças, receita |
| CEO | Diretor executivo | Alçada executiva |
| BOARD | Founder Board | Alçada máxima |

---

## 2. Gatilhos de aprovação (por característica da solicitação)

Aprovadores são **acumulados** conforme os `flags` da `GovernanceRequest`:

| Gatilho (flag) | Aprovador adicionado |
|---|---|
| _Sempre_ | OWNER |
| `involves_ai` | AI_OFFICER |
| `involves_personal_data` OU `involves_sensitive_data` | DPO |
| `involves_security` OU `involves_production_environment` | CTO + CISO |
| `involves_legal_contract` | LEGAL |
| `involves_financial_impact` | CFO |
| `risk_level == HIGH` | CEO |
| `risk_level == CRITICAL` | BOARD |

> A lista final é deduplicada (`unique(approvers)`).

---

## 3. Alçadas por nível de risco (resumo)

| Nível | Aprovação mínima |
|---|---|
| LOW | OWNER (+ especialistas conforme flags) |
| MEDIUM | OWNER + especialistas de domínio |
| HIGH | OWNER + especialistas + **CEO** |
| CRITICAL | OWNER + especialistas + CEO + **Founder Board** |

---

## 4. RACI por tipo de processo

**R** = Responsável (executa) · **A** = Aprova (alçada) · **C** = Consultado · **I** = Informado

| Processo | OWNER | AI_OFFICER | DPO | CTO | CISO | LEGAL | CFO | CEO | BOARD |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Novo produto SaaS | R | C | C | C | C | C | C | A | I |
| Criar/atualizar agente de IA | R | A | C | C | C | — | — | I | C¹ |
| Desativar agente / kill switch | R | A | I | A | A | — | — | I | I |
| Processamento de dado pessoal | R | C | A | C | C | C | — | I | — |
| Mudança em produção | R | C | — | A | A | — | — | I | — |
| Integração de API | R | C | C | A | A | — | — | I | — |
| Onboarding de fornecedor crítico | R | — | C | C | C | C | C | I | A |
| Contrato legal | R | — | C | — | — | A | C | I | — |
| Operação financeira | R | — | — | — | — | C | A | I | — |
| Incidente HIGH/CRITICAL | R | C² | C² | C | A | C | C | A | I³ |
| Alegação de marketing⁴ | R | C | — | — | — | A | — | C | — |

¹ Board obrigatório para agentes de autonomia `LEVEL_5_CRITICAL_AUTONOMOUS_ACTION`.
² Quando o incidente envolve IA ou dados.
³ Board informado em incidentes CRITICAL; convocado se houver violação de dados.
⁴ `INVARIANT 8`: alegações sobre "tecnologia proprietária", "ROI", "autonomia",
"custo marginal zero" ou "resultado garantido" exigem revisão legal + compliance.

---

## 5. Fluxo de decisão

```
Para cada aprovador exigido (em ordem):
    solicita decisão → registra evidência "APPROVAL_DECISION"
    REJECTED     → encerra fluxo como REJEITADO
    NEEDS_REVIEW → encerra fluxo como EM_REVISÃO
Se todos aprovam → APROVADO, solicitação segue para planejamento/execução.
```

Toda decisão gera um registro imutável no [Cofre de Evidências](../WSS13-SGI-AI-PSEUDOCODE-001.md#18-cofre-de-evidências).
