# Runbook — Continuidade e Recuperação de Desastres — WSS+13

> Operacionaliza o `ContinuityEngine` (seção 17). Suporta ISO 27001 (A.5.29–A.5.30),
> SOC 2 (Availability) e NIST CSF (Recover). Classificação: `INTERNAL_PROPRIETARY`.

| Campo | Valor |
|---|---|
| Documento | `WSS13-RB-DR-001` |
| Dono | COO / CISO |
| Teste | Trimestral (`disaster_recovery_test`) |

## 1. Sistemas críticos
Cada sistema crítico define **RTO** (tempo máximo para restaurar) e **RPO** (perda máxima de
dados aceitável), mantidos em `registro-de-ativos-de-dados.csv` / inventário de sistemas.

## 2. Requisitos por sistema crítico (`validate_business_continuity`)
- [ ] RTO definido · [ ] RPO definido
- [ ] Backup habilitado · [ ] Restore testado
- [ ] Monitoramento habilitado
- [ ] Runbook de incidente existente
- [ ] Contingência de fornecedor definida

## 3. Procedimento de recuperação
1. Declarar desastre e acionar comandante (integra o runbook de incidentes).
2. Iniciar `start_restore_procedure` a partir do backup íntegro mais recente.
3. Medir `recovery_time` e `data_loss`.
4. Validar integridade e reabrir o serviço.

## 4. Teste de DR (trimestral)
`disaster_recovery_test(system_id)`: simula falha, executa restore, mede tempos.
- Se `recovery_time > RTO` → não conformidade "RTO excedido".
- Se `data_loss > RPO` → não conformidade "RPO excedido".
Cada teste gera evidência `DISASTER_RECOVERY_TESTED` e alimenta melhoria contínua.

## 5. Dependência de fornecedores
Fornecedores críticos exigem plano de saída ou fornecedor reserva
(`backup_vendor_or_exit_plan`) — ver
[gestão de fornecedores](../../WSS13-SGI-AI-PSEUDOCODE-001.md#15-gestão-de-fornecedores-e-terceiros).
