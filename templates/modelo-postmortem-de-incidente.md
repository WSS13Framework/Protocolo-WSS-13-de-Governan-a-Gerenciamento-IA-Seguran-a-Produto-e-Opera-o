# Postmortem de Incidente — WSS13-INC-YYYY-NNNN

> Modelo do `MODULE IncidentEngine` (`handle_incident`). `INVARIANT 9`: todo incidente tem
> dono, severidade, linha do tempo, causa raiz e ações corretivas.

## Identificação
- **ID:** WSS13-INC-YYYY-NNNN
- **Título:**
- **Severidade (`IncidentSeverity`):** _(SEV_1_CRITICAL | SEV_2_HIGH | SEV_3_MEDIUM | SEV_4_LOW)_
- **Tipo:** _(SECURITY | PRIVACY | AI | OPERATIONAL | FINANCIAL …)_
- **Comandante do incidente:**

## Escopo
- **Sistemas afetados:**
- **Clientes afetados:**
- [ ] Suspeita de violação de dados (`data_breach_suspected`)
- [ ] Falha de IA envolvida (`ai_failure_involved`)
- [ ] Notificação regulatória exigida (`regulatory_notification_required`)

## Linha do tempo
| Horário | Evento |
|---|---|
| `started_at` | |
| `detected_at` | |
| … | Contenção |
| … | Recuperação |
| `resolved_at` | |

## Causa raiz
_Análise da causa raiz (`root_cause`)._

## Ações corretivas (CAPA)
| Ação | Dono | Prazo | Status |
|---|---|---|---|
| | | | |

## Lições aprendidas
_Alimenta o `ImprovementEngine`._
