# Política de Privacidade e Proteção de Dados — WSS+13

> Suporta LGPD, GDPR e ISO/IEC 27701. Deriva do `DataGovernanceEngine` (seção 10).
> Classificação: `INTERNAL_PROPRIETARY`.

| Campo | Valor |
|---|---|
| Documento | `WSS13-POL-PRIV-001` |
| Dono | DPO |
| Revisão | Anual + a cada novo tratamento relevante |

## 1. Princípio
**Privacidade por padrão** (`MANDATORY_PRINCIPLES`). Nenhum dado pessoal é tratado sem base
legal, finalidade, retenção e controle de acesso (`INVARIANT 6`).

## 2. Bases legais
Consentimento, execução de contrato, obrigação legal e legítimo interesse — registradas por
ativo de dado (ver [classificação de dados](../classificacao-de-dados-lgpd.md)).

## 3. Registro de operações de tratamento (RoPA)
Todo tratamento de dado pessoal é inventariado em
[`registro-de-operacoes-de-tratamento-ropa.csv`](../../../registers/registro-de-operacoes-de-tratamento-ropa.csv),
com finalidade, base legal, categorias de titulares e dados, retenção e transferências.

## 4. DPIA / RIPD
Obrigatória quando `requires_dpia` — dado sensível, larga escala, novas tecnologias de IA ou
risco residual elevado. Ver [modelo de DPIA](../../../templates/modelo-dpia.md).

## 5. Direitos dos titulares
Acesso, portabilidade, correção, eliminação, revogação de consentimento e informação sobre
tratamento — atendidos no ciclo de vida do cliente (seção 13). Prazo interno de atendimento: 15 dias.

## 6. Retenção e eliminação
Cada ativo define `retention_period_days` e `deletion_policy`. Dados expirados são eliminados
ou anonimizados; a eliminação gera evidência.

## 7. Transferência internacional
Fornecedores que tratam dado pessoal exigem DPA assinado, lista de subprocessadores e avaliação
de transferência internacional (`assess_vendor_data_processing_role`).

## 8. Incidente de dados
Suspeita de violação abre incidente e avalia `regulatory_notification_required` (notificação à
ANPD/autoridade e aos titulares quando aplicável), conforme o
[runbook de incidentes](../runbooks/runbook-resposta-a-incidentes.md).
