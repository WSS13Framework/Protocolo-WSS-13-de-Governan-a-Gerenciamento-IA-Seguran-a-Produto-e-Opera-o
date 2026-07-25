# WSS+13 SGI-AI OS

**Sistema de Gestão Integrado para Empresa de Inteligência Artificial**

> Ativo interno estratégico da WSS+13 — Governança, Gerenciamento, IA, Segurança, Produto e Operação.

---

## O que é

O **WSS+13 SGI-AI OS** (também referido como `WSS13_GOS` — *Governance Operating System*) é o
sistema operacional interno de governança da WSS+13. Ele define como **entra, é triado, executado,
aprovado, entregue, monitorado e melhorado** tudo o que acontece na empresa: produtos, agentes de IA,
dados, segurança, clientes, fornecedores, finanças, incidentes e auditoria.

### Princípio central

> Nada entra, muda, executa, integra, coleta dados, opera agentes, afeta clientes ou vai para
> produção **sem registro, responsável, classificação de risco, aprovação, evidência e monitoramento**.

```
Toda entrada gera ID.
Todo ID tem responsável.
Todo responsável segue processo.
Todo processo gera evidência.
Toda evidência alimenta auditoria.
Toda auditoria gera melhoria.
Toda melhoria fortalece o ativo WSS+13.
```

---

## Estrutura do repositório

```
.
├── README.md                                    # Este arquivo
├── CHANGELOG.md                                 # Controle de versão do ativo
├── docs/
│   ├── WSS13-SGI-AI-PSEUDOCODE-001.md            # Documento mestre do protocolo (v1.0.0)
│   └── governance/                              # Framework de governança operacional
│       ├── matriz-de-riscos.md
│       ├── matriz-de-aprovacao.md               # Alçadas / RACI
│       ├── catalogo-de-agentes-ia.md            # Framework dos 191 agentes
│       ├── classificacao-de-dados-lgpd.md
│       └── mapa-de-conformidade.md              # ISO / SOC 2 / NIST / LGPD / GDPR / EU AI Act
├── registers/                                   # Registros vivos (CSV)
│   ├── catalogo-agentes.csv
│   ├── registro-de-riscos.csv
│   ├── registro-de-fornecedores.csv
│   └── registro-de-ativos-de-dados.csv
├── templates/                                   # Modelos operacionais
│   ├── modelo-solicitacao-de-governanca.md
│   ├── modelo-avaliacao-de-risco.md
│   ├── modelo-dpia.md
│   └── modelo-postmortem-de-incidente.md
└── impl/                                        # Implementação de referência (WSS13_GOS)
    ├── wss13_gos/                               # Motores: intake, triage, risk, approval, evidence
    ├── tests/                                   # 21 testes (unittest, sem dependências)
    ├── run_demo.py                              # Demonstração ponta a ponta
    └── README.md
```

A implementação de referência é executável com Python 3.11+ (só stdlib):
`cd impl && python3 -m unittest discover -s tests` · `python3 run_demo.py` ·
`python3 -m wss13_gos.api`. Detalhes em [`impl/README.md`](./impl/README.md).

O documento mestre é o **pseudocódigo corporativo** que serve de base para transformar em:

- Documento interno de governança e manual operacional;
- Workflow em ClickUp, Jira, Linear ou Notion;
- Motor interno de automação / módulo administrativo da plataforma;
- Base de auditoria para ISO 9001, ISO 27001, ISO 27701, ISO 42001, SOC 2, NIST AI RMF e LGPD/GDPR;
- Ativo intelectual proprietário da empresa.

---

## Identificação do ativo

| Campo | Valor |
|---|---|
| `DOCUMENT_ID` | `WSS13-SGI-AI-PSEUDOCODE-001` |
| `VERSION` | `1.0.0` |
| `SYSTEM_NAME` | WSS+13 Governance Operating System |
| `SHORT_NAME` | `WSS13_GOS` |
| `CLASSIFICATION` | `INTERNAL_PROPRIETARY` — Confidencial / Propriedade intelectual da WSS+13 |
| `OWNER` | WSS+13 Founder Board |

---

## Padrões de governança visados

ISO 9001 · ISO 27001 · ISO 27701 · ISO 42001 · SOC 2 · NIST AI RMF ·
NIST Cybersecurity Framework · OWASP ASVS · OWASP Top 10 · OWASP LLM Top 10 ·
LGPD · GDPR Readiness · EU AI Act Readiness

---

## Roadmap

Programa de construção do ativo, em fases sequenciais:

| Fase | Objetivo | Status |
|:--:|---|---|
| **0** | Camada de governança operacional (matrizes, catálogo, conformidade, modelos) | ✅ Entregue |
| **1** | Implementação de referência do software (motores Intake/Risk/Approval/Evidence) | ✅ Entregue |
| **2** | Aprofundar governança para prontidão formal de auditoria ISO/SOC 2 | ✅ Entregue |
| **3** | Catalogar os 191 agentes (esqueleto + validador; dados reais a preencher) | ✅ Entregue |
| **4** | Fechar o ciclo: Incidentes, Auditoria e Painel Executivo | ✅ Entregue |

## Aviso de propriedade intelectual

Toda a lógica de governança, orquestração de agentes, mapas de processo, metodologias de diagnóstico,
métodos de pontuação, taxonomias internas, estruturas de evidência e fluxos de auditoria descritos
neste repositório são **propriedade intelectual da WSS+13**. Acesso restrito e confidencial.
