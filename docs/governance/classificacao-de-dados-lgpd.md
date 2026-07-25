# Classificação de Dados, LGPD e GDPR — WSS+13 SGI-AI OS

> Deriva do `MODULE DataGovernanceEngine` (seção 10), `ENTITY Dataset` e `ENUM DataClassification`.
> Classificação: `INTERNAL_PROPRIETARY`.

Nenhum dado é usado sem base legal, finalidade, regra de retenção e controle de acesso
(`INVARIANT 6`). Privacidade por padrão é um princípio obrigatório (`MANDATORY_PRINCIPLES`).

---

## 1. Níveis de classificação

| Nível | Exemplos | Controles mínimos |
|---|---|---|
| `PUBLIC` | Material de marketing publicado | — |
| `INTERNAL` | Documentos internos, métricas | Acesso por RBAC |
| `CONFIDENTIAL` | Contratos, dados de negócio | RBAC + criptografia em trânsito |
| `SENSITIVE` / `RESTRICTED` | Segredos de cliente, dados críticos | RBAC + cripto em repouso e trânsito + logs |
| `PERSONAL_DATA` | Dado pessoal (LGPD/GDPR) | Base legal + finalidade + retenção + minimização |
| `SENSITIVE_PERSONAL_DATA` | Dado pessoal sensível | Tudo acima + **aprovação do DPO** + controles reforçados |
| `CLIENT_SECRET` | Chaves/segredos de cliente | Cofre de segredos + rotação |
| `CRITICAL_SYSTEM_DATA` | Dados de sistema críticos | Segregação + backup + DR testado |

---

## 2. Validações obrigatórias por ativo de dado

Para cada `DataAsset` envolvido, o motor valida: dono, classificação, base legal, finalidade,
minimização, retenção, controle de acesso, criptografia (repouso + trânsito), política de backup
e política de exclusão. Dados **sensíveis** exigem aprovação do DPO e controles reforçados.

---

## 3. Bases legais (LGPD Art. 7º / GDPR Art. 6)

| Base legal | Uso típico na WSS+13 |
|---|---|
| Consentimento | Marketing, comunicações opcionais |
| Execução de contrato | Prestação do serviço SaaS ao cliente |
| Obrigação legal | Retenção fiscal, obrigações regulatórias |
| Legítimo interesse | Segurança, prevenção a fraude, melhoria de produto |

> Toda base legal é registrada no ativo de dado e verificada na avaliação de risco.

---

## 4. DPIA / RIPD (`run_dpia`)

Uma **Avaliação de Impacto à Proteção de Dados** é obrigatória quando `requires_dpia` é verdadeiro
(tratamento de dado sensível, larga escala, novas tecnologias de IA, ou risco residual elevado).

Conteúdo mínimo: ativos de dados, finalidade, base legal, riscos de privacidade, mitigações e
risco residual. Se o **risco residual for CRITICAL**, exige aprovação de Founder Board + Legal + DPO.
DPIA aprovada é arquivada como evidência (`store_artifact`). Ver
[modelo de DPIA](../../templates/modelo-dpia.md).

---

## 5. Direitos dos titulares

Processos de atendimento a titulares (integrados ao ciclo de vida do cliente):

| Direito | Onde é atendido |
|---|---|
| Acesso / portabilidade | Exportação de dados (`export_data_if_requested`) |
| Eliminação / esquecimento | Agendamento de exclusão (`schedule_data_deletion`) |
| Retenção | Aplicação de política (`apply_retention_policy`) |
| Revogação de acesso | Offboarding (`revoke_api_keys`, `disable_user_access`) |

---

## 6. Transferência internacional

Fornecedores que tratam dado pessoal exigem **DPA assinado**, lista de subprocessadores e
avaliação de transferência internacional (ver
[gestão de fornecedores](../WSS13-SGI-AI-PSEUDOCODE-001.md#15-gestão-de-fornecedores-e-terceiros)).
