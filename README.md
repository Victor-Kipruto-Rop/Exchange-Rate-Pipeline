# 🏗️ Exchange Rate Pipeline

A production-grade data engineering pipeline that fetches USD-based exchange rates daily, loads them into PostgreSQL, performs data quality checks, and transforms data through a dbt medallion architecture (staging → intermediate → marts).

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────┐    ┌──────────┐
│  API Source  │───▶│  Extract &    │───▶│  Data Quality   │───▶│  Load   │───▶│   dbt    │
│  (Exchange   │    │  Validate     │    │  Checks        │    │  to PG  │    │ Transform│
│   Rates)     │    │  (Airflow)    │    │  (Custom)      │    │         │    │          │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────┘    └────┬─────┘
                                                                                  │
                    ┌──────────────┐    ┌──────────────┐                          │
                    │  Slack Alert  │◀───│   Monitor     │◀─────────────────────────┘
                    │  (if KES Δ)  │    │   & Alert     │
                    └──────────────┘    └──────────────┘
```

## Project Structure

```
airflow-pipeline/
├── dags/                    # Airflow DAG definitions
│   ├── exchange_rate_dag.py # Main DAG with full pipeline orchestration
│   └── config.py           # Centralized DAG configuration
├── tasks/                   # Modular task functions
│   ├── extract_rates.py     # API extraction with retry & validation
│   ├── load_to_postgres.py  # Idempotent loading with upsert logic
│   ├── data_quality.py      # Data quality validation checks
│   └── trigger_dbt.py       # dbt execution wrapper
├── plugins/                 # Custom Airflow plugins
│   ├── slack_alert.py       # Slack notification with rich formatting
│   └── callbacks.py         # Task lifecycle callbacks
├── dbt_project/             # dbt transformation layer
│   ├── models/
│   │   ├── staging/         # Raw data ingestion (1:1 with source)
│   │   ├── intermediate/    # Business logic & cleaning
│   │   └── marts/           # Analytical output tables
│   └── macros/              # Reusable SQL macros
├── tests/                   # Unit and integration tests
├── scripts/                 # Operational scripts
├── config/                  # Configuration files
├── docker-compose.yml       # Containerized infrastructure
├── Makefile                 # Common operations
└── .env.example             # Environment variables template
```

## Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Orchestration | Apache Airflow 2.8 | DAG execution, scheduling, monitoring |
| Storage | PostgreSQL 15 | Data warehouse |
| Transformation | dbt-core | SQL-based transformations with testing |
| Monitoring | Slack Webhooks | Real-time pipeline alerts |
| Infrastructure | Docker Compose | Reproducible environment |
| Testing | pytest | Unit and integration tests |

## Data Quality Framework

- **Schema validation**: Ensures API response matches expected structure
- **Completeness checks**: Validates no missing required fields
- **Freshness checks**: Ensures data is current
- **Referential integrity**: Validates currency codes exist
- **dbt tests**: Unique, not_null, accepted_values, relationships

## Quickstart

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- (Optional) Slack webhook URL for alerts

### 1. Clone and configure

```bash
cd airflow-pipeline
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start infrastructure

```bash
make up          # Start all services
make init        # Initialize Airflow DB and create admin user
```

### 3. Access services

| Service | URL | Credentials |
|---------|-----|-------------|
| Airflow | http://localhost:8080 | admin / admin |
| PostgreSQL | localhost:5432 | admin / admin |

### 4. Run the pipeline

```bash
make trigger      # Trigger DAG manually
make test         # Run unit tests
make test-dbt     # Run dbt tests
make quality      # Run data quality checks
```

## Operations

```bash
make help              # Show all available commands
make logs              # View Airflow logs
make status            # Check service health
make dbt-run           # Run dbt models only
make dbt-test          # Run dbt tests only
make clean             # Remove containers and volumes
make lint              # Run code linting
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AIRFLOW__CORE__EXECUTOR` | `LocalExecutor` | Airflow executor type |
| `EXCHANGE_API_KEY` | - | API key (if required) |
| `SLACK_WEBHOOK_URL` | - | Slack incoming webhook URL |
| `KES_CHANGE_THRESHOLD` | `0.01` | KES change alert threshold (1%) |
| `POSTGRES_HOST` | `postgres` | Database host |
| `POSTGRES_DB` | `rates_db` | Database name |

### dbt Configuration

dbt profiles are configured via environment variables in `dbt_project/profiles.yml`. The schema defaults to `analytics` and can be overridden per environment.

## Monitoring & Alerting

- **Slack Alerts**: Fires on DAG failures and when KES moves > 1% day-over-day
- **Task Callbacks**: Custom success/failure handlers with contextual information
- **SLA Miss Alerts**: Configured per-task with 2-hour SLA
- **Data Quality Reports**: Logged to Airflow task logs

## Testing

```bash
# Unit tests
make test

# Integration tests (requires running infrastructure)
make test-integration

# dbt model tests
make test-dbt

# Data quality validation
make quality
```

## Deployment

### Production Considerations

1. **Executor**: Switch to `CeleryExecutor` or `KubernetesExecutor` for horizontal scaling
2. **Database**: Use managed PostgreSQL (RDS, Cloud SQL)
3. **Secrets**: Use Airflow Connections/Variables or external secrets manager (Vault, AWS Secrets Manager)
4. **Monitoring**: Add Prometheus metrics exporter and Grafana dashboards
5. **CI/CD**: GitHub Actions for automated testing and deployment

## License

MIT
## Tech Stack

| Technology | Purpose |
|------------|---------|
| Apache Airflow | Pipeline Orchestration |
| PostgreSQL | Metadata & Task Storage |
| dbt | Data Transformation |
| Docker | Containerization |

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Apache Airflow | Pipeline Orchestration |
| PostgreSQL | Metadata & Task Storage |
| dbt | Data Transformation |
| Docker | Containerization |
