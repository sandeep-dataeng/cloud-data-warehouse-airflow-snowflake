# Test plan

**Status: planned; tests have not yet been executed.**

- Airflow DAG parses successfully in the target Airflow/provider environment.
- Snowflake connection succeeds using the configured Airflow connection.
- Staging load handles empty, malformed and duplicate input.
- Duplicate business keys are rejected or deterministically resolved before SCD2.
- New business keys create one current dimension row.
- Changed tracked attributes expire the old row and create one new current row.
- Unchanged records do not create unnecessary dimension versions.
- Multiple changes for the same key in one batch are handled deterministically.
- Re-running the same batch is idempotent.
- Task retries, failure handling and alerting behave as configured.
- Source, staging, accepted, rejected and target counts reconcile.
