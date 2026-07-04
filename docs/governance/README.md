# Framework de Governança — WSS+13 SGI-AI OS

Índice dos artefatos de governança operacional derivados do
[documento mestre](../WSS13-SGI-AI-PSEUDOCODE-001.md).

## Matrizes e catálogos
- [Matriz de riscos](./matriz-de-riscos.md) — pontuação, faixas e cadência.
- [Matriz de aprovação / alçadas (RACI)](./matriz-de-aprovacao.md).
- [Catálogo dos 191 agentes de IA](./catalogo-de-agentes-ia.md).
- [Classificação de dados, LGPD e GDPR](./classificacao-de-dados-lgpd.md).
- [Mapa de conformidade](./mapa-de-conformidade.md) — ISO / SOC 2 / NIST / LGPD / GDPR / EU AI Act.

## Políticas (`policies/`)
- [Segurança da informação](./policies/politica-de-seguranca-da-informacao.md) — ISO 27001, SOC 2.
- [Gestão de IA responsável](./policies/politica-de-gestao-de-ia.md) — ISO 42001, NIST AI RMF, EU AI Act.
- [Controle de acesso](./policies/politica-de-controle-de-acesso.md) — ISO 27001, SOC 2.
- [Privacidade e proteção de dados](./policies/politica-de-privacidade-e-protecao-de-dados.md) — LGPD, GDPR, ISO 27701.

## Runbooks (`runbooks/`)
- [Resposta a incidentes](./runbooks/runbook-resposta-a-incidentes.md).
- [Continuidade e recuperação de desastres](./runbooks/runbook-recuperacao-de-desastres.md).

## Registros (`../../registers/`)
| Registro | Uso |
|---|---|
| `catalogo-agentes.csv` | Inventário dos 191 agentes |
| `registro-de-riscos.csv` | Riscos avaliados (`RiskRegisterDB`) |
| `registro-de-fornecedores.csv` | Fornecedores e criticidade |
| `registro-de-ativos-de-dados.csv` | Ativos de dados e classificação |
| `registro-de-operacoes-de-tratamento-ropa.csv` | RoPA (LGPD/GDPR) |
| `registro-de-revisao-de-acessos.csv` | Revisões periódicas de acesso |
| `declaracao-de-aplicabilidade-iso27001.csv` | SoA ISO 27001 |

## Notas de completude

Estes artefatos são a **base estruturada** do SGI. Antes de uma certificação formal, ainda é
necessário **operar e evidenciar** os controles ao longo do tempo. Em particular:

- A **SoA ISO 27001** contém apenas controles-âncora representativos; deve ser completada para
  todos os 93 controles do Anexo A (2022), com decisão de aplicabilidade justificada por controle.
- Os **registros** (RoPA, riscos, fornecedores, acessos) começam vazios e devem refletir a
  operação real.
- Treinamento, conscientização e período de observação de controles (SOC 2) são atividades
  contínuas, não geráveis por documento.
