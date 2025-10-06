#!/usr/bin/env python3
import boto3
import pytest
from botocore.exceptions import ClientError

def test_no_login_profiles_exist():
    """Test that no IAM login profiles exist after destroy"""
    iam = boto3.client('iam', region_name='us-east-1')
    
    # Check student users
    for i in range(1, 19):  # 18 students
        username = f"aluno-BigData-{i}"
        try:
            iam.get_login_profile(UserName=username)
            pytest.fail(f"Login profile still exists for {username}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                pass  # Expected - login profile should not exist
            else:
                pytest.fail(f"Error checking login profile for {username}: {e}")
    
    # Check teacher user
    try:
        iam.get_login_profile(UserName="professor-BigData")
        pytest.fail("Login profile still exists for professor-BigData")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            pass  # Expected - login profile should not exist
        else:
            pytest.fail(f"Error checking login profile for professor-BigData: {e}")

def test_dynamodb_credentials_empty():
    """Test that DynamoDB credentials table is empty after destroy"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    try:
        table = dynamodb.Table('iesb-student-credentials')
        response = table.scan()
        
        assert len(response['Items']) == 0, f"DynamoDB table should be empty but contains {len(response['Items'])} items"
        
    except ClientError as e:
        pytest.fail(f"Error scanning DynamoDB table: {e}")

def test_infrastructure_still_exists():
    """Test that core infrastructure still exists after credential destroy"""
    # Test DynamoDB table exists
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    try:
        table = dynamodb.Table('iesb-student-credentials')
        table.load()
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            pytest.fail("DynamoDB table should still exist after credential destroy")
    
    # Test users still exist
    iam = boto3.client('iam', region_name='us-east-1')
    for i in range(1, 19):
        username = f"aluno-BigData-{i}"
        try:
            iam.get_user(UserName=username)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                pytest.fail(f"User {username} should still exist after credential destroy")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
