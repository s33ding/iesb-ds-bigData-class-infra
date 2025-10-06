#!/usr/bin/env python3

"""
Trigger S3 Crawler - Simple Glue job to start the S3 crawler
"""

import boto3
import sys
from awsglue.utils import getResolvedOptions

# Get job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Glue client
glue_client = boto3.client('glue')

try:
    # Start the S3 crawler
    response = glue_client.start_crawler(Name='iesb-s3-crawler')
    print("✓ S3 Crawler started successfully")
    
except Exception as e:
    print(f"✗ Error starting crawler: {str(e)}")
    sys.exit(1)

print("Crawler trigger job completed!")
