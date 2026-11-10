# Airflow and Snowflake execution runbook

## Prerequisites
- A supported Airflow installation with compatible Snowflake provider.
- Airflow connection ID `snowflake_default` configured with database, schema, warehouse, role and authentication.
- The target schema created and the SQL DDL applied.
- Python dependencies installed in the Airflow environment.

## Suggested setup
1. Install Airflow using the official constraints file for your Python version.
2. Install a compatible `apache-airflow-providers-snowflake` release.
3. Copy this repository into a location accessible to the Airflow scheduler and workers.
4. Set the DAG folder and template search path so the DAG can locate the SQL scripts.
5. Configure `snowflake_default` through Airflow Connections or a secrets backend.
6. Run `sql/01_create_objects.sql` in a development schema.
7. Enable and trigger `cloud_warehouse_etl_starter`.

## Data loading
The `scripts/load_customers.py` helper reads the synthetic CSV and inserts rows into `STG_CUSTOMER`. It uses a batch ID to make retries of the same sample batch repeatable. Test this in a development schema before using it with any other data source.

## Data quality
Run `sql/03_data_quality_checks.sql` after loading. Resolve duplicates and invalid records before SCD processing.

## SCD Type 2
Review `sql/02_scd_type2_merge.sql` and validate its behavior against new, changed, unchanged and duplicate customer records. The sample SQL is illustrative and needs production-grade batch filtering and deterministic source deduplication before production use.

## Operational checks
Inspect task logs, loaded row counts, rejected records, current dimension row uniqueness, retry behavior and source-to-target reconciliation.

## Security
Never commit Airflow connection exports, passwords, private keys, tokens or account secrets.
