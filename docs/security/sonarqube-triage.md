# Triagem SonarCloud — datacosmos-br/OdooConnectorAPI

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead: `ai-hub-31k0.1`

## Resumo

**4 issues** — BLOCKER 0, CRITICAL 1, MAJOR 2, MINOR 1
Tipos: VULNERABILITY 4, BUG 0, CODE_SMELL 0 · **Debt total: 155min**

| regra | issues |
|---|---|
| `docker:S6470` | 1 |
| `docker:S8541` | 1 |
| `docker:S8544` | 1 |
| `docker:S6471` | 1 |

## Como usar

Cada issue traz a **mensagem do SonarQube** (descreve o problema e o impacto), o **código real** (linha `>>>`), o tipo e o effort estimado.
**Decisão**: `corrigir` / `falso-positivo` (marcar na plataforma com justificativa) / `risco-aceito`. Ordem: BLOCKER → CRITICAL → VULNERABILITY → MAJOR. CODE_SMELL em volume pede correção de padrão.

## Issues

### 1 · 🟠 CRITICAL · VULNERABILITY · `docker:S6470`
**Local**: `Dockerfile:8` · **Effort**: 20min

> Copying recursively might inadvertently add sensitive data to the container. Make sure it is safe here.

```
        4  # Set the working directory in the container
        5  WORKDIR /usr/src/app
        6  
        7  # Copy the current directory contents into the container at /usr/src/app
>>>     8  COPY . .
        9  
       10  # Install any needed packages specified in requirements.txt
       11  RUN pip install --no-cache-dir -r requirements.txt
       12  
```

**Decisão**: 

### 2 · 🟡 MAJOR · VULNERABILITY · `docker:S8541`
**Local**: `Dockerfile:11` · **Effort**: 1h

> Omitting "--only-binary :all:" can lead to the execution of setup scripts. Make sure it is safe here.

```
        7  # Copy the current directory contents into the container at /usr/src/app
        8  COPY . .
        9  
       10  # Install any needed packages specified in requirements.txt
>>>    11  RUN pip install --no-cache-dir -r requirements.txt
       12  
       13  # Make port 8000 available to the world outside this container
       14  EXPOSE 8000
       15  
```

**Decisão**: 

### 3 · 🟡 MAJOR · VULNERABILITY · `docker:S8544`
**Local**: `Dockerfile:11` · **Effort**: 1h

> Using dependencies without locking resolved versions is security-sensitive.

```
        7  # Copy the current directory contents into the container at /usr/src/app
        8  COPY . .
        9  
       10  # Install any needed packages specified in requirements.txt
>>>    11  RUN pip install --no-cache-dir -r requirements.txt
       12  
       13  # Make port 8000 available to the world outside this container
       14  EXPOSE 8000
       15  
```

**Decisão**: 

### 4 · ⚪ MINOR · VULNERABILITY · `docker:S6471`
**Local**: `Dockerfile:2` · **Effort**: 15min

> The "python" image runs with "root" as the default user. Make sure it is safe here.

```
        1  # Use a official Python runtime as a parent image
>>>     2  FROM python:3.12-slim
        3  
        4  # Set the working directory in the container
        5  WORKDIR /usr/src/app
        6  
```

**Decisão**: 

