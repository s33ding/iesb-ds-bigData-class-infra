#!/usr/bin/env python3

"""
Bronze Layer ETL - IESB BigData Class
Creates bronze layer from PostgreSQL tables with proper partitioning and metadata
"""

import sys
import boto3
import json
from datetime import datetime
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import current_timestamp, lit

# Get job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Get credentials from Secrets Manager
secrets_client = boto3.client('secretsmanager')
secret = secrets_client.get_secret_value(SecretId='rds-secret')
credentials = json.loads(secret['SecretString'])

# Bronze layer configuration
BUCKET = "iesb-bigdata"
BRONZE_PATH = f"s3://{BUCKET}/bronze"
BATCH_DATE = datetime.now().strftime("%Y-%m-%d")

# Table list - simplified structure
tables = [
    "municipio", "unidade_federacao", "regiao", "municipio_ride_brasilia",
    "ed_enem_2024_resultados", "ed_enem_2024_participantes", "educacao_basica", 
    "censo_escolar_2024", "ed_superior_cursos", "ed_superior_ies", 
    "ed_enem_2024_resultados_amos_per", "sus_aih", "sus_procedimento_ambulatorial",
    "Censo_20222_Populacao_Idade_Sexo", "agregados_setores_censitarios",
    "pib_municipios", "ocorrencia"
]

print(f"Starting Bronze Layer ETL - Batch Date: {BATCH_DATE}")

# Process all tables in single bronze folder
for table_name in tables:
    try:
        print(f"Processing table: {table_name}")
        
        # Read from PostgreSQL
        df = spark.read.jdbc(
            url=jdbc_url,
            table=table_name,
            properties=connection_properties
        )
        
        # Add metadata columns
        df_with_metadata = df \
            .withColumn("bronze_load_date", lit(BATCH_DATE)) \
            .withColumn("bronze_load_timestamp", current_timestamp()) \
            .withColumn("source_system", lit("postgresql"))
        
        # Write to bronze layer - single level
        output_path = f"{BRONZE_PATH}/{table_name}"
        
        df_with_metadata.write \
            .mode("overwrite") \
            .partitionBy("bronze_load_date") \
            .parquet(output_path)
        
        # Get record count for logging
        record_count = df.count()
        print(f"✓ {table_name}: {record_count} records -> {output_path}")
        
    except Exception as e:
        print(f"✗ Error processing {table_name}: {str(e)}")
        continue

print(f"\n=== Bronze Layer ETL Completed ===")

# Trigger crawler to update catalog
try:
    glue_client = boto3.client('glue')
    glue_client.start_crawler(Name='iesb-s3-crawler')
    print("✓ S3 Crawler triggered to update catalog")
except Exception as e:
    print(f"⚠ Could not trigger crawler: {str(e)}")

job.commit()
