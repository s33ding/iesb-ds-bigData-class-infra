#!/usr/bin/env python3
import boto3
import pytest
from botocore.exceptions import ClientError

def test_dynamodb_table_exists():
    """Test that DynamoDB credentials table exists"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    try:
        table = dynamodb.Table('iesb-student-credentials')
        table.load()
        assert True, "DynamoDB table exists"
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            pytest.fail("DynamoDB table does not exist")
        else:
            pytest.fail(f"Error accessing DynamoDB table: {e}")

def test_no_login_profiles_exist():
    """Test that no IAM login profiles exist for students"""
    iam = boto3.client('iam', region_name='us-east-1')
    
    # Check student users
    for i in range(1, 19):  # 18 students
        username = f"aluno-BigData-{i}"
        try:
            iam.get_login_profile(UserName=username)
            pytest.fail(f"Login profile still exists for {username}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                # This is expected - login profile should not exist
                pass
            else:
                pytest.fail(f"Error checking login profile for {username}: {e}")
    
    # Check teacher user
    try:
        iam.get_login_profile(UserName="professor-BigData")
        pytest.fail("Login profile still exists for professor-BigData")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            # This is expected - login profile should not exist
            pass
        else:
            pytest.fail(f"Error checking login profile for professor-BigData: {e}")

def test_users_still_exist():
    """Test that IAM users still exist (only login profiles should be destroyed)"""
    iam = boto3.client('iam', region_name='us-east-1')
    
    # Check student users exist
    for i in range(1, 19):  # 18 students
        username = f"aluno-BigData-{i}"
        try:
            iam.get_user(UserName=username)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                pytest.fail(f"User {username} does not exist")
            else:
                pytest.fail(f"Error checking user {username}: {e}")
    
    # Check teacher user exists
    try:
        iam.get_user(UserName="professor-BigData")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            pytest.fail("User professor-BigData does not exist")
        else:
            pytest.fail(f"Error checking user professor-BigData: {e}")

def test_dynamodb_credentials_empty():
    """Test that DynamoDB credentials table is empty"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    try:
        table = dynamodb.Table('iesb-student-credentials')
        response = table.scan()
        
        assert len(response['Items']) == 0, f"DynamoDB table should be empty but contains {len(response['Items'])} items"
        
    except ClientError as e:
        pytest.fail(f"Error scanning DynamoDB table: {e}")

def test_sns_topic_exists():
    """Test that SNS topic for credentials notifications exists"""
    sns = boto3.client('sns', region_name='us-east-1')
    
    try:
        response = sns.list_topics()
        topic_arns = [topic['TopicArn'] for topic in response['Topics']]
        
        expected_topic = 'arn:aws:sns:us-east-1:248189947068:bigdata-students-cred'
        assert any(expected_topic in arn for arn in topic_arns), f"SNS topic {expected_topic} not found"
        
    except ClientError as e:
        pytest.fail(f"Error listing SNS topics: {e}")

def test_s3_buckets_exist():
    """Test that required S3 buckets exist"""
    s3 = boto3.client('s3', region_name='us-east-1')
    
    required_buckets = ['iesb-bigdata', 'dataiesb-sysadmin']
    
    try:
        response = s3.list_buckets()
        existing_buckets = [bucket['Name'] for bucket in response['Buckets']]
        
        for bucket in required_buckets:
            assert bucket in existing_buckets, f"Required bucket {bucket} does not exist"
            
    except ClientError as e:
        pytest.fail(f"Error listing S3 buckets: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
