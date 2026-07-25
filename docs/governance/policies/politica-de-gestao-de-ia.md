# Política de Gestão de IA Responsável — WSS+13

> Suporta ISO/IEC 42001, NIST AI RMF, OWASP LLM Top 10 e EU AI Act (readiness).
> Deriva do `AIGovernanceEngine` (seção 9). Classificação: `INTERNAL_PROPRIETARY`.

| Campo | Valor |
|---|---|
| Documento | `WSS13-POL-AI-001` |
| Dono | AI Officer |
| Aprovação | Founder Board |
| Revisão | Trimestral (`quarterly_strategic_review`) |

## 1. Princípio
**IA responsável por padrão** (`MANDATORY_PRINCIPLES`). Nenhum agente opera em produção sem
registro no catálogo, dono, nível de risco, logs e registro de avaliação (`INVARIANT 4`).

## 2. Classificação de autonomia e supervisão
Todo agente recebe um `AIAutonomyLevel` (0 a 5). Requisitos por nível estão no
[catálogo de agentes](../catalogo-de-agentes-ia.md). Agentes `LEVEL_5_CRITICAL_AUTONOMOUS_ACTION`
exigem aprovação de Founder Board + CISO + DPO + AI Officer, kill switch, override humano e logs
completos.

## 3. Avaliação obrigatória antes de produção
Suíte mínima (`run_agent_evaluation_suite`): prompt injection, vazamento de dados, alucinação,
viés, abuso de ferramentas, isolamento entre clientes, consistência, alinhamento de negócio e
fronteiras de segurança. Agentes HIGH/CRITICAL exigem **red team** adicional.

## 4. Limites e thresholds
Cada agente define `hallucination_threshold`, `bias_threshold` e `failure_threshold`
monitorados continuamente. Ultrapassar o limite dispara revisão e pode acionar o kill switch.

## 5. Kill switch e resposta
Acionável por CEO, CTO, CISO ou AI Officer. Aciona `DISABLED_EMERGENCY`, bloqueia execução,
registra evidência e abre incidente `AI_INCIDENT`.

## 6. Transparência (EU AI Act readiness)
Sistemas de IA voltados a usuários finais devem indicar que são IA e registrar decisões
relevantes para rastreabilidade e supervisão humana.

## 7. Auditoria
`audit_ai_agents` (mensal) verifica dono, risco, autonomia, versão de prompt, revisão, kill
switch, fontes de dados, ferramentas e métricas — e, para HIGH/CRITICAL, aprovação humana, red
team concluído e logs completos.
