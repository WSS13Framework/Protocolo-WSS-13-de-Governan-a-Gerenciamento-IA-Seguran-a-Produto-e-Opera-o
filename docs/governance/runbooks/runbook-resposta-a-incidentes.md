# Runbook — Resposta a Incidentes — WSS+13

> Operacionaliza o `IncidentEngine` (seção 16) e o `INVARIANT 9`.
> Suporta ISO 27001 (A.5.24–A.5.28), SOC 2 e NIST CSF (Respond/Recover).

| Campo | Valor |
|---|---|
| Documento | `WSS13-RB-INC-001` |
| Dono | CISO |

## 1. Severidades e alvos de resposta
| Severidade | Exemplo | Reconhecimento | Comunicação |
|---|---|---|---|
| `SEV_1_CRITICAL` | Vazamento de dados, produção fora | ≤ 15 min | Founder Board imediato |
| `SEV_2_HIGH` | Falha de IA em produção, brecha contida | ≤ 1 h | CTO/CISO |
| `SEV_3_MEDIUM` | Degradação parcial | ≤ 4 h | Dono do sistema |
| `SEV_4_LOW` | Impacto mínimo | ≤ 1 dia | Registro |

## 2. Fluxo (`handle_incident`)
1. **Abertura** — `open_incident(type, severity, description)`; atribui comandante; abre sala se HIGH/CRITICAL.
2. **Classificação** — tipo (SECURITY/PRIVACY/AI/…), sistemas e clientes afetados.
3. **Contenção** — isolar; para IA, acionar `kill_switch` se necessário.
4. **Preservação de evidências** — logs, snapshots (não destruir rastros).
5. **Erradicação** — remover causa raiz.
6. **Recuperação** — restaurar serviço e validar.
7. **Comunicação** — clientes/reguladores se `regulatory_notification_required`.
8. **Postmortem** — usar [modelo](../../../templates/modelo-postmortem-de-incidente.md); gerar CAPA no `ImprovementEngine`.

## 3. Notificação regulatória (LGPD/GDPR)
Suspeita de violação de dado pessoal → DPO avalia notificação à autoridade e aos titulares.
Registrar decisão e prazo como evidência.

## 4. Encerramento
Incidente só fecha com causa raiz documentada, ações corretivas atribuídas e postmortem
arquivado. Evidência `INCIDENT_CLOSED` registrada pelo comandante.
