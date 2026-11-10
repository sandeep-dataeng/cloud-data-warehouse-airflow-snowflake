"""Starter Airflow DAG for loading and validating Snowflake customer data.

Configure snowflake_default before enabling this DAG. SQL files are resolved
through the DAG's template search path.
"""
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from scripts.load_customers import load_customers_to_staging
from scripts.validate_staging import validate_staging

PROJECT_ROOT = str(Path(__file__).resolve().parents[1])

with DAG(
    dag_id="cloud_warehouse_etl_starter",
    description="Load synthetic customer data and validate Snowflake staging",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    template_searchpath=[PROJECT_ROOT],
    tags=["portfolio", "snowflake", "etl"],
) as dag:
    start = EmptyOperator(task_id="start")

    create_objects = SQLExecuteQueryOperator(
        task_id="create_warehouse_objects",
        conn_id="snowflake_default",
        sql="sql/01_create_objects.sql",
    )

    load_staging = PythonOperator(
        task_id="load_customers_to_staging",
        python_callable=load_customers_to_staging,
    )

    quality_check = PythonOperator(
        task_id="validate_staging_data",
        python_callable=validate_staging,
    )

    apply_scd2 = SQLExecuteQueryOperator(
        task_id="apply_scd_type2",
        conn_id="snowflake_default",
        sql="sql/02_scd_type2_merge.sql",
    )

    finish = EmptyOperator(task_id="finish")
    start >> create_objects >> load_staging >> quality_check >> apply_scd2 >> finish
