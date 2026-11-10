# Architecture and engineering notes

## Pipeline stages
1. **Source:** synthetic CSV extracts represent incoming customer data.
2. **Orchestration:** Airflow DAG defines dependencies, scheduling, retries and task logs.
3. **Staging:** Snowflake staging table receives source records with batch metadata in a future implementation.
4. **Validation:** check required fields, types, duplicate business keys and rejected records.
5. **Transformation:** standardize attributes and prepare dimension/fact records.
6. **Warehouse:** maintain analytical dimensions and facts; SCD Type 2 tracks historical changes.

## SCD Type 2 model
A dimension row includes a business key, effective start, effective end and current-row flag. When tracked attributes change, expire the current row and insert a new version. Ensure one source row per business key per batch and handle multiple changes deterministically.

## Reliability
- Design tasks to be safe to retry.
- Use a batch ID or source watermark for incremental processing.
- Record source, accepted, rejected and target row counts.
- Define backfill and late-arriving data behavior.
- Avoid partial updates using appropriate transactions/atomic patterns.

## Security
Use Airflow Connections or a secrets backend and least-privilege Snowflake roles. Never put credentials in DAG source, SQL files or logs.

## Validate before production use
Airflow/provider compatibility, Snowflake authentication, source ingestion mechanism, watermark strategy, SCD2 edge cases, warehouse sizing, alerting and deployment.
