"""Fail the Airflow task when basic staging quality checks fail."""
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


def validate_staging(snowflake_conn_id="snowflake_default"):
    hook = SnowflakeHook(snowflake_conn_id=snowflake_conn_id)
    connection = hook.get_conn()
    checks = {
        "missing_required_fields": """
            SELECT COUNT(*) FROM STG_CUSTOMER
            WHERE CUSTOMER_ID IS NULL OR TRIM(CUSTOMER_ID) = ''
               OR CUSTOMER_NAME IS NULL OR UPDATED_AT IS NULL
        """,
        "duplicate_batch_customer": """
            SELECT COUNT(*) FROM (
                SELECT BATCH_ID, CUSTOMER_ID
                FROM STG_CUSTOMER
                GROUP BY BATCH_ID, CUSTOMER_ID
                HAVING COUNT(*) > 1
            )
        """,
    }
    try:
        with connection.cursor() as cursor:
            failures = {}
            for name, sql in checks.items():
                cursor.execute(sql)
                count = cursor.fetchone()[0]
                if count:
                    failures[name] = count
        if failures:
            raise ValueError(f"Staging data quality checks failed: {failures}")
        return "Staging quality checks passed"
    finally:
        connection.close()
