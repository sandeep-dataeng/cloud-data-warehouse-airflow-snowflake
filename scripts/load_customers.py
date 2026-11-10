"""Airflow task helper: load the portfolio CSV into Snowflake staging.

The Airflow Snowflake connection must be configured as snowflake_default.
This loader uses a batch ID to make retries of the same sample batch repeatable.
"""
import csv
from pathlib import Path

from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

DEFAULT_FILE = Path(__file__).resolve().parents[1] / "data" / "customers_sample.csv"


def load_customers_to_staging(
    csv_path=str(DEFAULT_FILE),
    snowflake_conn_id="snowflake_default",
):
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            rows.append((
                row["CUSTOMER_ID"],
                row["CUSTOMER_NAME"],
                row["EMAIL"],
                row["CITY"],
                row["UPDATED_AT"],
                row["BATCH_ID"],
            ))

    if not rows:
        raise ValueError("Input CSV contains no customer records")

    hook = SnowflakeHook(snowflake_conn_id=snowflake_conn_id)
    connection = hook.get_conn()
    try:
        with connection.cursor() as cursor:
            batch_ids = sorted({row[5] for row in rows})
            if len(batch_ids) != 1:
                raise ValueError("This sample loader expects exactly one batch ID")

            # Delete-and-reload the same batch so a task retry is repeatable.
            cursor.execute(
                "DELETE FROM STG_CUSTOMER WHERE BATCH_ID = %s",
                (batch_ids[0],),
            )
            cursor.executemany(
                """
                INSERT INTO STG_CUSTOMER
                (CUSTOMER_ID, CUSTOMER_NAME, EMAIL, CITY, UPDATED_AT, BATCH_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                rows,
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {"loaded_rows": len(rows), "batch_id": batch_ids[0]}
