#!/usr/bin/env python3
import boto3

def get_account_id():
    """Get AWS account ID"""
    try:
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']
    except Exception as e:
        print(f"Error getting account ID: {e}")
        return "ACCOUNT_ID"

def print_student_links():
    """Print essential AWS service links for students"""
    account_id = get_account_id()
    region = "us-east-1"
    
    print("=" * 60)
    print("AWS BIGDATA CLASS - STUDENT LINKS")
    print("=" * 60)
    print(f"Account ID: {account_id}")
    print(f"Region: {region}")
    print(f"Console: https://{account_id}.signin.aws.amazon.com/console?region={region}")
    print()
    
    print("GLUE:")
    print(f"Jobs: https://{region}.console.aws.amazon.com/glue/home#etl:tab=jobs")
    print(f"Crawlers: https://{region}.console.aws.amazon.com/glue/home#catalog:tab=crawlers")
    print(f"Databases: https://{region}.console.aws.amazon.com/glue/home#catalog:tab=databases")
    print()
    
    print("ATHENA:")
    print(f"Query Editor: https://{region}.console.aws.amazon.com/athena/home#/query-editor")
    print()
    
    print("S3:")
    print(f"Class Bucket: https://{region}.console.aws.amazon.com/s3/buckets/iesb-bigdata/")
    print()
    
    print("PERFORMANCE INSIGHTS:")
    print(f"RDS PI: https://{region}.console.aws.amazon.com/rds/home#performance-insights-v20206:")
    print("=" * 60)

if __name__ == "__main__":
    print_student_links()
