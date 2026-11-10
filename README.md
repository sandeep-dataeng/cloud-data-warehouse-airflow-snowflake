# Cloud Data Warehouse & ETL Orchestration Platform

**Technologies:** Apache Airflow | Snowflake | Python | SQL | PySpark | Delta Lake

## Project Overview

This project demonstrates the design of a cloud-based data warehouse pipeline using Apache Airflow for workflow orchestration and Snowflake for analytical data storage and transformation.

The pipeline is designed to ingest source data, perform data validation and transformation, load warehouse tables, and maintain historical records using Slowly Changing Dimension (SCD) Type 2.

## Architecture

```text
Source Files (CSV / JSON)
          |
          v
   Apache Airflow
   (Orchestration)
          |
          v
    Data Ingestion
          |
          v
   Snowflake Staging
          |
          v
 Data Validation & Transformation
          |
          v
   Dimension & Fact Tables
          |
          v
  Analytics / Reporting
```

## Key Components

### 1. Apache Airflow
- Workflow orchestration using DAGs.
- Task dependencies and scheduling.
- Retry mechanisms and failure handling.
- Pipeline monitoring and execution logs.

### 2. Snowflake
- Database, schema, warehouse and table management.
- Staging and analytical data models.
- SQL-based transformations.
- Incremental data processing.
- Slowly Changing Dimension (SCD) Type 2.

### 3. Python and SQL
- Data ingestion and processing.
- Data validation and transformation.
- SQL-based warehouse operations.
- Data quality checks.

### 4. Data Engineering Concepts
- ETL/ELT pipeline design.
- Incremental loading.
- Data warehouse modelling.
- Idempotent processing.
- Error handling and data reconciliation.

## Repository Structure

```text
cloud-data-warehouse-airflow-snowflake/
│
├── dags/
│   └── warehouse_pipeline.py
│
├── sql/
│   ├── 01_create_objects.sql
│   └── 02_scd_type2_merge.sql
│
├── data/
│   └── customers_sample.csv
│
├── docs/
│   └── architecture.md
│
├── tests/
│   └── TEST_PLAN.md
│
├── requirements.txt
└── README.md
```

## Implementation Status

This repository currently contains the initial project scaffold, sample data, architecture documentation, starter Airflow DAG and SQL examples.

The live Airflow and Snowflake integration, end-to-end execution, and testing are planned validation steps and should not be considered completed yet.

## Future Enhancements

- Implement end-to-end ingestion.
- Add incremental loading with watermark logic.
- Implement and test SCD Type 2.
- Add data quality and reconciliation checks.
- Configure Airflow monitoring and alerting.
- Add automated testing and CI/CD.

---

**Note:** This is an independent learning and portfolio project using synthetic sample data. No employer or client data, credentials, or proprietary code are included.
