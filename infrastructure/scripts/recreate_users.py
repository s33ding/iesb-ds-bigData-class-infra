#!/usr/bin/env python3
import subprocess
import sys
import os
import boto3
from botocore.exceptions import ClientError

def run_terraform_command(command, cwd="../tf"):
    """Run terraform command and return result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, result.stderr, 0
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def check_users_exist():
    """Check if any users exist that need to be destroyed"""
    iam = boto3.client('iam')
    users_to_check = []
    
    # Add student users
    for i in range(1, 19):  # 18 students
        users_to_check.append(f"aluno-BigData-{i}")
    
    # Add teacher user
    users_to_check.append("professor-BigData")
    
    existing_users = []
    for username in users_to_check:
        try:
            iam.get_user(UserName=username)
            existing_users.append(username)
        except ClientError as e:
            if e.response['Error']['Code'] != 'NoSuchEntity':
                print(f"Error checking user {username}: {e}")
    
    return existing_users

def recreate_users():
    """Recreate all users by destroying and applying user resources"""
    print("Starting user recreation process...")
    
    # Change to terraform directory
    tf_dir = "../tf"
    if not os.path.exists(tf_dir):
        print(f"Error: Terraform directory {tf_dir} not found")
        return False
    
    # Check if users exist before trying to destroy
    existing_users = check_users_exist()
    
    if existing_users:
        print(f"\n1. Found {len(existing_users)} existing users. Destroying them...")
        
        # Target destroy user resources
        destroy_targets = [
            "aws_iam_user.students",
            "aws_iam_user.teacher", 
            "aws_iam_user_login_profile.students",
            "aws_iam_user_login_profile.teacher",
            "aws_iam_user_group_membership.students",
            "aws_iam_user_group_membership.teacher"
        ]
        
        for target in destroy_targets:
            print(f"Destroying {target}...")
            stdout, stderr, returncode = run_terraform_command(f"terraform destroy -target={target} -auto-approve")
            
            if returncode != 0 and "No objects need to be destroyed" not in stdout:
                print(f"Warning: Failed to destroy {target}")
                print(f"Error: {stderr}")
            else:
                print(f"Successfully processed {target}")
    else:
        print("\n1. No existing users found. Skipping destroy step...")
    
    print("\n2. Creating user resources...")
    
    # Apply to create users
    stdout, stderr, returncode = run_terraform_command("terraform apply -auto-approve")
    
    if returncode != 0:
        print("Error: Failed to create users")
        print(f"Error output: {stderr}")
        return False
    
    print("Successfully created all users!")
    
    print("\n3. Exporting new credentials...")
    
    # Run the credential export script
    try:
        export_stdout, export_stderr, export_returncode = run_terraform_command("python3 export_credentials.py")
        
        if export_returncode != 0:
            print("Warning: Failed to export credentials")
            print(f"Error: {export_stderr}")
        else:
            print("Credentials exported successfully!")
    except Exception as e:
        print(f"Warning: Could not run credential export: {e}")
    
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("Usage: python recreate_users.py")
        print("This script will:")
        print("1. Destroy existing IAM users and login profiles")
        print("2. Recreate them using Terraform")
        print("3. Export new credentials to DynamoDB")
        return
    
    print("WARNING: This will destroy and recreate all student and teacher users!")
    print("All existing user sessions will be invalidated.")
    
    confirm = input("Do you want to continue? (yes/no): ").lower().strip()
    
    if confirm != 'yes':
        print("Operation cancelled.")
        return
    
    success = recreate_users()
    
    if success:
        print("\n✅ User recreation completed successfully!")
        print("New credentials have been generated and stored in DynamoDB.")
        print("Run 'python get_user_creds.py' to view the new credentials.")
    else:
        print("\n❌ User recreation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
