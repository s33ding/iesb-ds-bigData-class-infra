#!/usr/bin/env python3
import boto3
import pytest
from botocore.exceptions import ClientError

def test_login_profiles_exist():
    """Test that IAM login profiles exist after create"""
    iam = boto3.client('iam', region_name='us-east-1')
    
    # Check student users
    for i in range(1, 19):  # 18 students
        username = f"aluno-BigData-{i}"
        try:
            profile = iam.get_login_profile(UserName=username)
            assert profile['LoginProfile']['UserName'] == username
            assert profile['LoginProfile']['PasswordResetRequired'] == False
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                pytest.fail(f"Login profile does not exist for {username}")
            else:
                pytest.fail(f"Error checking login profile for {username}: {e}")
    
    # Check teacher user
    try:
        profile = iam.get_login_profile(UserName="professor-BigData")
        assert profile['LoginProfile']['UserName'] == "professor-BigData"
        assert profile['LoginProfile']['PasswordResetRequired'] == False
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            pytest.fail("Login profile does not exist for professor-BigData")
        else:
            pytest.fail(f"Error checking login profile for professor-BigData: {e}")

def test_dynamodb_credentials_populated():
    """Test that DynamoDB credentials table has data after create"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    try:
        table = dynamodb.Table('iesb-student-credentials')
        response = table.scan()
        
        assert len(response['Items']) == 18, f"DynamoDB table should contain 18 items but has {len(response['Items'])}"
        
        # Verify each student has credentials
        usernames = [item['username'] for item in response['Items']]
        for i in range(1, 19):
            expected_username = f"aluno-BigData-{i}"
            assert expected_username in usernames, f"Missing credentials for {expected_username}"
            
        # Verify each item has required fields
        for item in response['Items']:
            assert 'username' in item, "Missing username field"
            assert 'temp_password' in item, "Missing temp_password field"
            assert len(item['temp_password']) > 0, "Password field is empty"
        
    except ClientError as e:
        pytest.fail(f"Error scanning DynamoDB table: {e}")

def test_users_and_groups_exist():
    """Test that users and groups exist after create"""
    iam = boto3.client('iam', region_name='us-east-1')
    
    # Test group exists
    try:
        group = iam.get_group(GroupName="iesb-bigdata-students")
        assert group['Group']['GroupName'] == "iesb-bigdata-students"
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            pytest.fail("Group iesb-bigdata-students does not exist")
    
    # Test users exist and are in group
    for i in range(1, 19):
        username = f"aluno-BigData-{i}"
        try:
            user = iam.get_user(UserName=username)
            assert user['User']['UserName'] == username
            
            # Check user is in group
            groups = iam.list_groups_for_user(UserName=username)
            group_names = [g['GroupName'] for g in groups['Groups']]
            assert "iesb-bigdata-students" in group_names, f"User {username} not in students group"
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                pytest.fail(f"User {username} does not exist")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
