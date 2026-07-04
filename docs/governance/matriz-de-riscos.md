# Matriz de Riscos — WSS+13 SGI-AI OS

> Derivada do `MODULE RiskEngine` (seção 7 do
> [documento mestre](../WSS13-SGI-AI-PSEUDOCODE-001.md)).
> Classificação: `INTERNAL_PROPRIETARY`.

Este documento operacionaliza a metodologia de risco do protocolo: como cada solicitação
(`GovernanceRequest`) é pontuada, classificada e encaminhada para os controles e aprovações
correspondentes.

---

## 1. Dimensões de risco avaliadas

Toda solicitação é pontuada em **8 dimensões**, cada uma numa escala inteira de **1 a 5**
(1 = risco desprezível, 5 = risco extremo).

| Dimensão | Campo | O que avalia |
|---|---|---|
| IA | `ai_risk_score` | Autonomia, alucinação, viés, uso indevido de ferramentas |
| Dados | `data_risk_score` | Dado pessoal/sensível, base legal, retenção, vazamento |
| Segurança | `security_risk_score` | Exposição, superfície de ataque, produção, segredos |
| Legal | `legal_risk_score` | Contrato, cláusula, alegação de marketing, regulatório |
| Financeiro | `financial_risk_score` | Impacto em receita, cobrança, reconciliação |
| Operacional | `operational_risk_score` | Continuidade, dependência, complexidade técnica |
| Reputacional | `reputation_risk_score` | Exposição de marca, cliente, mídia |
| Impacto no cliente | `client_impact_score` | Nº de clientes afetados e criticidade |

Além disso, avaliam-se **probabilidade** (`probability_score`, 1–5) e **impacto agregado**
(`impact_score`, 1–5).

---

## 2. Fórmula de pontuação (soma ponderada)

Os pesos refletem a prioridade estratégica da WSS+13: **dados e segurança acima de tudo**,
seguidos de IA e reputação.

```
total_score = ai_risk           × 1.4
            + data_risk          × 1.5
            + security_risk      × 1.5
            + legal_risk         × 1.3
            + financial_risk     × 1.1
            + operational_risk   × 1.0
            + reputation_risk    × 1.4
            + client_impact      × 1.2
            + probability        × 1.0
            + impact             × 1.5
```

**Faixa teórica:** mínimo `12.9` (todas as dimensões = 1) · máximo `64.5` (todas = 5).
As faixas de classificação abaixo usam a escala normalizada `0–100` adotada pelo protocolo.

---

## 3. Faixas de classificação (`classify_risk_level`)

| Faixa (`total_score`) | Nível | Cor | Postura |
|---|---|---|---|
| `≤ 25` | **LOW** | 🟢 | Fluxo padrão, aprovação do dono |
| `> 25 e ≤ 50` | **MEDIUM** | 🟡 | Revisão de área + controles adicionais |
| `> 50 e ≤ 75` | **HIGH** | 🟠 | Revisão executiva + CEO, kill switch para IA |
| `> 75` | **CRITICAL** | 🔴 | Founder Board, DPIA/red team obrigatórios |

---

## 4. Cadência de revisão por nível

Alinhada às constantes do protocolo (Apêndice A do documento mestre).

| Nível | Ciclo de revisão | Constante |
|---|---|---|
| LOW / MEDIUM | 30 dias | `DEFAULT_REVIEW_CYCLE_DAYS` |
| HIGH | 7 dias | `HIGH_RISK_REVIEW_CYCLE_DAYS` |
| CRITICAL | 1 dia | `CRITICAL_RISK_REVIEW_CYCLE_DAYS` |

---

## 5. Controles e revisões exigidos por nível

| Requisito | LOW | MEDIUM | HIGH | CRITICAL |
|---|:--:|:--:|:--:|:--:|
| Registro + dono + evidência | ✅ | ✅ | ✅ | ✅ |
| Avaliação de risco registrada | ✅ | ✅ | ✅ | ✅ |
| Revisão de segurança (`requires_security_review`) | — | condic. | ✅ | ✅ |
| Revisão de IA (`requires_ai_review`) | — | condic. | ✅ | ✅ |
| Revisão legal (`requires_legal_review`) | — | condic. | condic. | ✅ |
| DPIA (`requires_dpia`) | — | condic.¹ | condic.¹ | ✅¹ |
| Red team de IA | — | — | condic. | ✅ |
| Founder Board (`requires_founder_board`) | — | — | — | ✅ |
| Kill switch ativo (IA) | — | — | ✅ | ✅ |

¹ DPIA disparada sempre que houver dado pessoal/sensível, independente do nível — ver
[classificação de dados](./classificacao-de-dados-lgpd.md).

---

## 6. Matriz probabilidade × impacto (heatmap 5×5)

Referência visual para calibrar `probability_score` × `impact_score`.

| P \ I | 1 | 2 | 3 | 4 | 5 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| **5** | 🟡 | 🟠 | 🔴 | 🔴 | 🔴 |
| **4** | 🟡 | 🟡 | 🟠 | 🔴 | 🔴 |
| **3** | 🟢 | 🟡 | 🟡 | 🟠 | 🔴 |
| **2** | 🟢 | 🟢 | 🟡 | 🟡 | 🟠 |
| **1** | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 |

---

## 7. Registro de riscos

Riscos avaliados são persistidos em `RiskRegisterDB` e espelhados no registro operacional
[`registers/registro-de-riscos.csv`](../../registers/registro-de-riscos.csv), com o `risk_id`
no padrão `WSS13-RISK-YYYY-NNNN`.

Cada linha vincula-se a uma `GovernanceRequest` (`request_id`) e mantém: nível, pontuação total,
controles exigidos, aprovadores exigidos, risco residual e data da próxima revisão.
