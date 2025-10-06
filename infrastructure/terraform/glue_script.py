import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
import json

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_BUCKET'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Get RDS credentials from Secrets Manager
secrets_client = boto3.client('secretsmanager')
secret = secrets_client.get_secret_value(SecretId='rds-secret')
credentials = json.loads(secret['SecretString'])

# Read from RDS
df = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:mysql://{credentials['host']}:{credentials['port']}/{credentials['dbname']}") \
    .option("user", credentials['username']) \
    .option("password", credentials['password']) \
    .option("dbtable", "your_table") \
    .load()

# Write to S3
df.write \
    .mode("overwrite") \
    .parquet(f"s3://{args['S3_BUCKET']}/data/")

job.commit()
