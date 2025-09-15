import sys
import boto3
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Get credentials from Secrets Manager
secrets_client = boto3.client('secretsmanager')
secret = secrets_client.get_secret_value(SecretId='rds-read-only')
credentials = json.loads(secret['SecretString'])

# Table list
tables = [
    "municipio", "unidade_federacao", "regiao", "ed_enem_2024_resultados",
    "ed_enem_2024_participantes", "educacao_basica", "censo_escolar_2024",
    "pib_municipios", "sus_aih", "sus_procedimento_ambulatorial",
    "ed_superior_cursos", "ed_superior_ies", "agregados_setores_censitarios",
    "Censo_20222_Populacao_Idade_Sexo", "municipio_ride_brasilia",
    "ocorrencia", "ed_enem_2024_resultados_amos_per"
]

# JDBC connection properties using Secrets Manager
jdbc_url = f"jdbc:postgresql://{credentials['host']}:{credentials['port']}/{credentials['dbname']}"
connection_properties = {
    "user": credentials['username'],
    "password": credentials['password'],
    "driver": "org.postgresql.Driver"
}

for table_name in tables:
    # Read from PostgreSQL using Spark JDBC
    df = spark.read.jdbc(
        url=jdbc_url,
        table=table_name,
        properties=connection_properties
    )
    
    # Write to S3 as Parquet
    df.write.mode("overwrite").parquet(f"s3://iesb-bigdata-dya39x2g/postgres/{table_name}/")
    
    print(f"Table {table_name} exported to S3!")

job.commit()
