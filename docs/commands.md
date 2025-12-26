# Commands — Projeto Task Core

Este ficheiro documenta os comandos oficiais usados no projeto.

Não existem comandos “implícitos”.
Tudo o que é executado deve estar aqui documentado.

---

## Ambiente de Desenvolvimento (DEV)

### Subir ambiente DEV

Cria o ambiente PostgreSQL de desenvolvimento do zero:

```bash
scripts/dev_setup.sh
```

Este comando:
- sobe o container PostgreSQL (DEV)
- cria schema e tabelas
- aplica seed de desenvolvimento

### Reset completo do DEV

Remove completamente o ambiente DEV:

```bash
docker compose -f docker/docker-compose.dev.yml down -v
```

Depois disso, o ambiente pode ser recriado com:

```bash
scripts/dev_setup.sh
```

## Executar CLI (ambiente DEV)
A CLI existe apenas para:
- demonstrar o fluxo do domínio
- executar cenários pedagógicos
- tornar visíveis decisões via logs

```bash
uv run python main.py
```

Notas importantes:
- a CLI usa repositório em memória
- os dados não persistem entre execuções
- o estado é sempre recriado

Testes

Testes normais (default)

Incluem:
- testes de domínio
- testes da camada de aplicação

Não usam base de dados real.

```bash
uv run pytest
```

Estes testes:
- são seguros
- correm sempre
- não alteram infraestrutura

⸻

## Testes de infraestrutura (PostgreSQL)

⚠️ Nunca correm por defeito

Antes de executar:
- o ambiente TEST deve existir
- criado via script dedicado

Criar ambiente TEST:

```bash
scripts/test_setup.sh
```

Executar testes de infraestrutura:

```bash
RUN_INFRA_TESTS=1 uv run pytest -m infrastructure -v
```

Estes testes:
- usam PostgreSQL real
- criam e removem dados
- assumem isolamento
- nunca devem apontar para DEV ou PROD

⸻

## Estrutura do projeto

Visualizar a estrutura do projeto, ignorando ficheiros irrelevantes:

```bash
tree -a -I ".venv|__pycache__|.pytest_cache|.git|uv.lock|__init__.py"
```

## Regras importantes
- Nunca executar testes de infraestrutura sem isolamento
- Nunca apontar testes para DEV ou PROD
- Nunca criar ambientes manualmente fora dos scripts
- Scripts são a fonte de verdade operacional