# GDP ETL Quality Gate
### Uma pipeline de dados para obtenção de informações de PIB per capita da América do Sul com esteira automatizada de qualidade de código

> **Português** | [English below](#english-version)

---

## Sobre o projeto

Pipeline de ETL governado por esteira de qualidade de código, com o objetivo de estudar DevOps aplicado ao lakehouse e ao ambiente analítico.

Os dados são consumidos via API REST do World Bank, processados com PySpark seguindo a arquitetura medalhão (bronze → silver), e persistidos em formato parquet num storage account Azure simulado localmente via Azurite — tudo containerizado com Docker.

O repositório é governado no GitHub, onde a esteira de CI analisa cada contribuição automaticamente por meio de ferramentas de qualidade Python e scripts Linux.

---

## Arquitetura

```
World Bank API (REST)
        ↓
   extract.py          ← Python puro, busca os dados
        ↓
   load.py             ← PySpark, persiste bronze no Azurite
        ↓
   transform.py        ← PySpark, limpa e persiste silver
        ↓
Azurite (Docker)       ← Simula Azure Blob Storage localmente
        ↓
  data/bronze/         ← Dado bruto em parquet
  data/silver/         ← Dado tratado em parquet

Push no GitHub
        ↓
GitHub Actions (CI)
        ↓
run_quality.sh
        ↓
ruff → black → mypy
        ↓
✅ passa / ❌ bloqueia merge
```

---

## Stack

| Tecnologia | Papel |
|---|---|
| Python 3.12 | Linguagem principal |
| PySpark 4.1 | Motor de processamento |
| Docker + Docker Compose | Containerização e orquestração |
| Azurite | Emulador local do Azure Blob Storage |
| Jupyter + PySpark | Exploração e discovery dos dados |
| GitHub Actions | Esteira de CI/CD |
| ruff | Linting e code smell |
| black | Formatação de código |
| mypy | Checagem de tipos |
| Makefile | Atalhos de automação |

---

## Estrutura do projeto

```
gdp_etl_quality_gate/
│
├── etl/
│   ├── extract.py          # Consome a API do World Bank
│   ├── load.py             # Persiste a camada bronze no Azurite
│   ├── transform.py        # Limpa e persiste a camada silver
│   └── spark_session.py    # Cria e configura a SparkSession
│
├── scripts/
│   └── run_quality.sh      # Script Linux da esteira de qualidade
│
├── notebooks/              # Notebooks Jupyter para exploração (não versionados)
│
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline do GitHub Actions
│
├── Dockerfile              # Empacota o ETL
├── docker-compose.yml      # Orquestra Azurite + Jupyter
├── Makefile                # Atalhos: make run, make quality, make build
├── requirements.txt        # Dependências Python
├── .env.example            # Template de variáveis de ambiente
└── main.py                 # Orquestra extract → load → transform
```

---

## Como rodar

### Pré-requisitos
- Docker
- Docker Compose
- Make

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/YUmeda-82/gdp_etl_quality_gate
cd gdp_etl_quality_gate

# 2. Configure as variáveis de ambiente
cp .env.example .env

# 3. Sobe os containers (Azurite + Jupyter)
docker-compose up -d

# 4. Roda o pipeline ETL
make run

# 5. Valida a qualidade do código
make quality
```

### Exploração dos dados (opcional)
Acesse o Jupyter em `http://localhost:8888` com o token exibido em:
```bash
docker logs spark-notebook 2>&1 | grep token
```

---

## CI/CD

A esteira de qualidade é o coração do projeto.

A cada push ou Pull Request, o GitHub Actions sobe uma VM Ubuntu, instala as dependências e executa o script `scripts/run_quality.sh`:

```bash
ruff check etl/     # detecta code smells e imports não utilizados
black --check etl/  # verifica formatação
mypy etl/           # verifica tipos
```

**Branch Protection Rules** garantem que nenhum PR pode ser mergeado na `main` se a esteira falhar — simulando o fluxo de um time de engenharia real.

---

## Próximos passos

- [ ] Migrar de parquet para **Delta Lake** (ACID transactions, time travel)
- [ ] Provisionar infraestrutura com **Terraform**
- [ ] Adicionar testes unitários com **pytest**
- [ ] Implementar orquestração com **Apache Airflow**
- [ ] Observabilidade com **Prometheus + Grafana**

---

## English version

### GDP ETL Quality Gate

A DataOps pipeline consuming South American GDP per capita data from the World Bank REST API, processed with PySpark following the medallion architecture (bronze → silver), and persisted as parquet in a locally containerized Azure Blob Storage emulator (Azurite).

The repository is governed on GitHub with an automated CI pipeline that enforces code quality on every contribution — blocking merges if ruff, black, or mypy detect any issues.

**Tech stack:** Python · PySpark · Docker · Azurite · GitHub Actions · ruff · black · mypy

**Next steps:** Delta Lake · Terraform · pytest · Airflow · Observability