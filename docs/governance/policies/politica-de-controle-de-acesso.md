# Política de Controle de Acesso — WSS+13

> Suporta ISO/IEC 27001 (A.5/A.8) e SOC 2 (Security). Classificação: `INTERNAL_PROPRIETARY`.

| Campo | Valor |
|---|---|
| Documento | `WSS13-POL-AC-001` |
| Dono | CISO |
| Revisão | Trimestral + a cada onboarding/offboarding |

## 1. Princípios
- **Menor privilégio:** acesso mínimo necessário para a função.
- **Segregação de funções:** quem executa não aprova a própria alçada.
- **Need-to-know:** dados classificados (ver [classificação de dados](../classificacao-de-dados-lgpd.md)) só a quem precisa.

## 2. Modelo RBAC
Papéis mapeiam para permissões; usuários recebem papéis, nunca permissões avulsas. Papéis de
governança em [matriz de aprovação](../matriz-de-aprovacao.md).

## 3. Autenticação
- MFA obrigatório para acessos privilegiados e a produção.
- Chaves de API por cliente/serviço, com escopo e rotação.

## 4. Ciclo de vida do acesso
| Evento | Ação |
|---|---|
| Onboarding | Provisionamento por papel, registro de concessão |
| Mudança de função | Reavaliação de papéis |
| Offboarding | Revogação imediata (`revoke_api_keys`, `disable_user_access`) |
| Revisão periódica | Trimestral, registrada em `registro-de-revisao-de-acessos.csv` |

## 5. Acesso de agentes de IA
Agentes só acessam `data_sources_allowed` e `tools_allowed` declarados no catálogo. Acesso a
dado pessoal exige `can_access_personal_data = TRUE` e aprovação do DPO.

## 6. Evidência
Concessões, revogações e revisões de acesso geram evidência no cofre e são auditadas mensalmente
(`audit_access_reviews`).
