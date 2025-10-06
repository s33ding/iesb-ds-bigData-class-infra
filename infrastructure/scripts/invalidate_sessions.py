#!/usr/bin/env python3
import boto3
from botocore.exceptions import ClientError

def invalidate_user_sessions():
    """Delete all student and teacher users to force logout"""
    iam = boto3.client('iam')
    
    users_to_delete = []
    for i in range(1, 19):
        users_to_delete.append(f"aluno-BigData-{i}")
    users_to_delete.append("professor-BigData")
    
    deleted_count = 0
    
    for username in users_to_delete:
        try:
            # Remove from groups
            groups = iam.list_groups_for_user(UserName=username)
            for group in groups['Groups']:
                iam.remove_user_from_group(UserName=username, GroupName=group['GroupName'])
            
            # Delete access keys
            keys = iam.list_access_keys(UserName=username)
            for key in keys['AccessKeyMetadata']:
                iam.delete_access_key(UserName=username, AccessKeyId=key['AccessKeyId'])
            
            # Delete login profile
            try:
                iam.delete_login_profile(UserName=username)
            except ClientError:
                pass
            
            # Detach policies
            policies = iam.list_attached_user_policies(UserName=username)
            for policy in policies['AttachedPolicies']:
                iam.detach_user_policy(UserName=username, PolicyArn=policy['PolicyArn'])
            
            # Delete inline policies
            inline_policies = iam.list_user_policies(UserName=username)
            for policy_name in inline_policies['PolicyNames']:
                iam.delete_user_policy(UserName=username, PolicyName=policy_name)
            
            # Delete user
            iam.delete_user(UserName=username)
            deleted_count += 1
            print(f"Deleted user: {username}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                print(f"User {username} does not exist")
            else:
                print(f"Error deleting {username}: {e}")
    
    print(f"\nDeleted {deleted_count} users. All sessions are now terminated.")

if __name__ == "__main__":
    invalidate_user_sessions()
