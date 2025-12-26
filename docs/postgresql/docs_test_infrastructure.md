# TEST-INFRA — Testes de Infraestrutura

## Objetivo

Ambiente efémero para testes de infraestrutura automatizados.

Características:
	•	destrutivo
	•	isolado
	•	porta dinâmica
	•	sem volume persistente
	•	criado e destruído por execução

Usado apenas por:
	•	testes de infraestrutura
	•	CI (no futuro)

## Configuração
	•	Docker Compose project: test-infra-<uuid>
	•	PostgreSQL 16
	•	Porta: dinâmica

## Script oficial

```bash
scripts/test_infra_setup.sh
```

Este script:
	•	cria um PostgreSQL efémero
	•	aplica bootstrap e migrations
	•	executa os testes de infraestrutura
	•	destrói tudo no final

## Regras globais
	•	container_name não é usado
	•	isolamento é feito via docker compose -p
	•	infra tests nunca tocam em DEV ou TEST
	•	ambientes humanos nunca são destruídos automaticamente