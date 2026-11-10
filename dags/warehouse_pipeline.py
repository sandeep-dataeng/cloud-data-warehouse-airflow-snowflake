"""Starter Airflow DAG for a Snowflake warehouse workflow.

Configure the snowflake_default Airflow connection before enabling this DAG.
The SQL path must be available under Airflow's template search path.
"""
from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id="cloud_warehouse_etl_starter",
    description="Starter orchestration for a Snowflake warehouse pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["portfolio", "snowflake", "etl"],
) as dag:
    start = EmptyOperator(task_id="start")

    create_objects = SQLExecuteQueryOperator(
        task_id="create_warehouse_objects",
        conn_id="snowflake_default",
        sql="sql/01_create_objects.sql",
    )

    # TODO: Add source ingestion, staging validation, incremental watermark,
    # SCD processing, audit counts and failure-notification tasks.
    finish = EmptyOperator(task_id="finish")

    start >> create_objects >> finish
