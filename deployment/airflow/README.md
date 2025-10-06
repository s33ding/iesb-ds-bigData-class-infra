# Airflow DAGs and Scripts

This folder contains the Apache Airflow DAGs and supporting scripts for the IESB BigData class.

## Structure

- `dags/` - Airflow DAG definitions
- `scripts/` - Supporting Python scripts for Glue jobs
- `requirements.txt` - Python dependencies for Airflow

## DAGs

### bronze_layer_etl.py
Main ETL pipeline that:
1. Runs the bronze layer ETL Glue job
2. Waits for completion
3. Triggers the S3 crawler to update the data catalog

## Deployment

DAGs are automatically deployed to the Airflow environment via Terraform configuration in `../tf/airflow.tf`.
