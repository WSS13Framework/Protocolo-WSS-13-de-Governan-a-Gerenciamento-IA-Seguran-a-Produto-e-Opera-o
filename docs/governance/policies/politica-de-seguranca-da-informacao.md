# Política de Segurança da Informação — WSS+13

> Suporta ISO/IEC 27001 e SOC 2 (Security). Deriva do `SecurityEngine` (seção 11) e do
> `INVARIANT 3`. Classificação: `INTERNAL_PROPRIETARY`.

| Campo | Valor |
|---|---|
| Documento | `WSS13-POL-SEC-001` |
| Dono | CISO |
| Aprovação | Founder Board |
| Revisão | Anual ou após incidente CRITICAL |

## 1. Objetivo
Estabelecer os princípios e controles mínimos que protegem a confidencialidade, integridade e
disponibilidade das informações e sistemas da WSS+13. **Segurança por padrão** é princípio
obrigatório (`MANDATORY_PRINCIPLES`).

## 2. Escopo
Todos os colaboradores, fornecedores, sistemas, ambientes (`DEVELOPMENT`, `STAGING`,
`PRODUCTION`, `AUDIT_SANDBOX`) e dados sob responsabilidade da WSS+13.

## 3. Controles mínimos (validados por `validate_security_controls`)
| Controle | Exigência |
|---|---|
| MFA | Obrigatório para todo acesso privilegiado |
| RBAC | Acesso por menor privilégio, revisado periodicamente |
| Criptografia em trânsito | TLS em toda comunicação externa |
| Criptografia em repouso | Dados CONFIDENTIAL+ e pessoais |
| Gestão de segredos | Cofre de segredos, rotação, sem segredo em código |
| Segregação de ambientes | Produção isolada de dev/staging |
| Logging | Trilhas de auditoria habilitadas e imutáveis |
| Backup | Habilitado e testado (ver runbook de DR) |
| Rate limiting de API | Obrigatório em endpoints expostos |
| Monitoramento | Alertas de segurança 24×7 |

## 4. Entrega segura (DevSecOps, seção 11)
Nenhuma mudança em produção sem: ticket vinculado, avaliação de risco aprovada, proteção de
branch, PR revisado, testes, scan de segredos, scan de dependências, SAST, checagem de segurança
de API, plano de rollback e janela de deploy definida.

## 5. Resposta a incidentes
Incidentes seguem o [runbook de resposta a incidentes](../runbooks/runbook-resposta-a-incidentes.md)
e o `IncidentEngine` (seção 16). `INVARIANT 9`: todo incidente tem dono, severidade, linha do
tempo, causa raiz e ações corretivas.

## 6. Conformidade
Auditorias mensais (`run_monthly_audit`) verificam a aderência. Não conformidades geram CAPA
(`create_corrective_action`). Mapeamento de controles em
[mapa de conformidade](../mapa-de-conformidade.md).
