# Commands — Projeto Task Core

Este ficheiro documenta **todos os comandos oficiais** do projeto.

## Ambiente DEV

### Criar ambiente DEV
```bash
scripts/dev_setup.sh
```

### Reset completo do DEV

```bash
docker compose -p dev -f docker/docker-compose.dev.yml down -v --remove-orphans
```

## Ambiente TEST (estável)

### Criar / atualizar ambiente TEST

```bash
scripts/test_setup.sh
```

Este comando:
- é idempotente
- não apaga dados
- pode ser executado várias vezes

⸻

## Testes de Infraestrutura

### Executar infra tests

```bash
scripts/test_infra_setup.sh
```

Este é o único comando válido para infra tests.

## CLI (ambiente DEV)

### A CLI existe apenas para demonstrar o domínio.

```bash
uv run python -m app.interfaces.cli.main
```

## Testes unitários e de domínio

```bash
uv run pytest
```

## Estrutura do projeto

```bash
tree -a -I ".venv|__pycache__|.pytest_cache|.git|uv.lock|__init__.py"
```