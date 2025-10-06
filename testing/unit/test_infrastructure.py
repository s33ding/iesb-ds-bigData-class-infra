import boto3
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_iam_users():
    logger.debug("Testing IAM users...")
    iam = boto3.client('iam')
    
    try:
        users = iam.list_users()['Users']
        bigdata_users = [u for u in users if u['UserName'].startswith('aluno-BigData-')]
        
        logger.info(f"Found {len(bigdata_users)} BigData users:")
        for user in bigdata_users:
            logger.info(f"  - {user['UserName']}")
        
        assert len(bigdata_users) == 18, f"Expected 18 users, found {len(bigdata_users)}"
    except Exception as e:
        logger.error(f"IAM test failed: {e}")
        raise

def test_s3_buckets():
    logger.debug("Testing S3 buckets...")
    s3 = boto3.client('s3')
    
    try:
        buckets = s3.list_buckets()['Buckets']
        
        class_buckets = [b for b in buckets if b['Name'].startswith('iesb-bigdata-')]
        backend_buckets = [b for b in buckets if b['Name'] == 'tf-dataiesb-bigdata']
        
        logger.info(f"Class buckets: {[b['Name'] for b in class_buckets]}")
        logger.info(f"Backend bucket: {[b['Name'] for b in backend_buckets]}")
        
        assert len(class_buckets) >= 1, f"No class buckets found"
        assert len(backend_buckets) == 1, f"Backend bucket not found"
    except Exception as e:
        logger.error(f"S3 test failed: {e}")
        raise

def test_dynamodb_table():
    logger.debug("Testing DynamoDB table...")
    dynamodb = boto3.client('dynamodb')
    
    try:
        tables = dynamodb.list_tables()['TableNames']
        logger.info(f"DynamoDB tables: {tables}")
        
        assert 'iesb-student-credentials' in tables, "Credentials table not found"
    except Exception as e:
        logger.error(f"DynamoDB test failed: {e}")
        raise

def test_glue_job():
    logger.debug("Testing Glue job...")
    glue = boto3.client('glue')
    
    try:
        jobs = glue.get_jobs()['Jobs']
        job_names = [j['Name'] for j in jobs]
        
        logger.info(f"Glue jobs: {job_names}")
        assert 'iesb-rds-to-s3-job' in job_names, "RDS to S3 job not found"
    except Exception as e:
        logger.error(f"Glue test failed: {e}")
        raise
