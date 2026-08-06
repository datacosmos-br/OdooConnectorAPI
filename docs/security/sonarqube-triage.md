# Triagem SonarCloud — datacosmos-br/OdooConnectorAPI

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead de rastreio: `ai-hub-31k0.1`

## Resumo

**4 issues** — BLOCKER 0, CRITICAL 1, MAJOR 2, MINOR 1
Tipos: VULNERABILITY 4, BUG 0, CODE_SMELL 0

| regra | issues |
|---|---|
| `docker:S6470` | 1 |
| `docker:S8541` | 1 |
| `docker:S8544` | 1 |
| `docker:S6471` | 1 |

## Issues

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | tipo | regra | componente | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | VULNERABILITY | `docker:S6470` | `Dockerfile` | 8 | |
| 2 | MAJOR | VULNERABILITY | `docker:S8541` | `Dockerfile` | 11 | |
| 3 | MAJOR | VULNERABILITY | `docker:S8544` | `Dockerfile` | 11 | |
| 4 | MINOR | VULNERABILITY | `docker:S6471` | `Dockerfile` | 2 | |

## Como triar

1. **BLOCKER e CRITICAL primeiro**, e todo VULNERABILITY independente de severidade.
2. Classificar: **corrigir**, **falso-positivo** (marcar na plataforma SonarCloud com justificativa), **risco-aceito** (com prazo).
3. CODE_SMELL em volume alto sugere padrão — corrigir a causa raiz, não issue a issue.

Dados brutos: `~/sonarqube-violations/by-repo/datacosmos-br__OdooConnectorAPI.json`

