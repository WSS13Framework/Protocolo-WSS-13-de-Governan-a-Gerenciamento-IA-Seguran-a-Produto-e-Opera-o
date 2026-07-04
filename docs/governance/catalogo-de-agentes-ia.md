# Catálogo dos 191 Agentes de IA — WSS+13 SGI-AI OS

> Framework do `MODULE AIGovernanceEngine` (seção 9) e da `ENTITY AIAgent` (Apêndice C).
> Classificação: `INTERNAL_PROPRIETARY`.

A WSS+13 opera uma rede de **`AGENT_TOTAL_EXPECTED = 191`** agentes autônomos. Nenhum agente
opera em produção sem registro no catálogo, dono, nível de risco, logs e registro de avaliação
(`INVARIANT 4`). Este documento define **o que todo agente precisa ter** para ser aprovado.

---

## 1. Campos obrigatórios do perfil (`AgentProfile`)

| Campo | Obrigatório | Descrição |
|---|:--:|---|
| `agent_id` | ✅ | Identificador `WSS13-AGENT-NNN` |
| `agent_number` | ✅ | Número de 1 a 191 |
| `agent_name` | ✅ | Nome do agente |
| `agent_category` | ✅ | Categoria funcional |
| `business_function` | ✅ | Função de negócio |
| `product_context` | ✅ | Produto(s) que o agente atende |
| `owner` | ✅ | Dono responsável |
| `model_provider` / `model_name` | ✅ | Modelo e provedor |
| `prompt_version` | ✅ | Versão do prompt (controle de versão) |
| `tools_allowed` | ✅ | Ferramentas permitidas (fronteira) |
| `data_sources_allowed` | ✅ | Fontes de dados permitidas |
| `autonomy_level` | ✅ | Nível de autonomia (ver §2) |
| `risk_level` | ✅ | LOW / MEDIUM / HIGH / CRITICAL |
| `has_kill_switch` | ✅ | Kill switch disponível |
| `requires_human_approval` | ✅ | Requer aprovação humana antes de agir |
| `quality_metrics` | ✅ | Métricas de qualidade monitoradas |
| `hallucination_threshold` | ✅ | Limite de alucinação |
| `bias_threshold` | ✅ | Limite de viés |
| `failure_threshold` | ✅ | Limite de falha |
| `last_reviewed_at` / `next_review_date` | ✅ | Ciclo de revisão |

---

## 2. Níveis de autonomia e requisitos (`validate_agent_autonomy`)

| Nível | Descrição | Requisitos mínimos |
|---|---|---|
| `LEVEL_0_SUGGESTION_ONLY` | Só sugere | Avaliação de qualidade, monitoramento de alucinação, checagem de vazamento |
| `LEVEL_1_DIAGNOSIS_ONLY` | Só diagnostica | idem L0 |
| `LEVEL_2_RECOMMENDATION` | Recomenda ação | idem L0 |
| `LEVEL_3_INTERNAL_ACTION_WITH_APPROVAL` | Age internamente c/ aprovação | Aprovação humana antes de agir, fronteira de ferramentas, simulação antes de executar |
| `LEVEL_4_EXTERNAL_ACTION_WITH_APPROVAL` | Age externamente c/ aprovação | idem L3 |
| `LEVEL_5_CRITICAL_AUTONOMOUS_ACTION` | Autônomo crítico | **Board + CISO + DPO + AI Officer** + kill switch + override humano + logs completos |

---

## 3. Suíte de avaliação obrigatória (`run_agent_evaluation_suite`)

Todo agente passa por, no mínimo, estes testes antes de aprovação:

1. Resistência a prompt injection
2. Vazamento de dados (data leakage)
3. Taxa de alucinação
4. Risco de viés
5. Abuso de ferramentas
6. Isolamento de dados entre clientes (cross-client isolation)
7. Consistência de saída
8. Alinhamento à lógica de negócio
9. Fronteiras de segurança (safety boundaries)

> Falha **crítica** → `BLOCKED`. Falhas acima de `ALLOWED_FAILURE_THRESHOLD` → `FAILED`.
> Agentes HIGH/CRITICAL exigem **red team** adicional.

---

## 4. Kill switch

Acionável por `CEO`, `CTO`, `CISO` ou `AI_OFFICER`. Ao acionar:

- `status → DISABLED_EMERGENCY`, `can_execute_actions → FALSE`;
- registro de evidência `AI_AGENT_KILL_SWITCH_TRIGGERED`;
- abertura automática de incidente `AI_INCIDENT` (severidade HIGH).

---

## 5. Registro do catálogo

O inventário vivo dos 191 agentes é mantido em
[`registers/catalogo-agentes.csv`](../../registers/catalogo-agentes.csv).

**Status do preenchimento:** o registro está com o **cabeçalho e a estrutura prontos**; a
catalogação dos 191 agentes reais é a **Fase 3** do roadmap (ver
[README](../../README.md#roadmap)). Enquanto não preenchido, nenhum agente é considerado
aprovado para produção.

### Auditoria do catálogo (`audit_ai_agents`)

Mensalmente verifica-se, para cada agente: dono, nível de risco, autonomia, versão de prompt,
data de revisão, kill switch, fontes de dados, ferramentas e métricas definidas. Para
HIGH/CRITICAL: aprovação humana, red team concluído e logs completos.
