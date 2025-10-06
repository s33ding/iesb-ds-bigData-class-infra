#!/usr/bin/env python3
import boto3
import sys

def get_account_id():
    """Get AWS account ID"""
    try:
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']
    except Exception as e:
        print(f"Error getting account ID: {e}")
        return "UNKNOWN"

def get_all_credentials():
    """Get all user credentials from DynamoDB table"""
    dynamodb = boto3.client('dynamodb')
    
    try:
        response = dynamodb.scan(TableName='iesb-student-credentials')
        
        credentials = []
        for item in response['Items']:
            credentials.append({
                'username': item['username']['S'],
                'temp_password': item['temp_password']['S']
            })
        
        # Handle pagination if needed
        while 'LastEvaluatedKey' in response:
            response = dynamodb.scan(
                TableName='iesb-student-credentials',
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            for item in response['Items']:
                credentials.append({
                    'username': item['username']['S'],
                    'temp_password': item['temp_password']['S']
                })
        
        return sorted(credentials, key=lambda x: int(x['username'].split('-')[-1]))
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_user_credentials(username):
    """Get user credentials from DynamoDB table"""
    dynamodb = boto3.client('dynamodb')
    
    try:
        response = dynamodb.get_item(
            TableName='iesb-student-credentials',
            Key={'username': {'S': username}}
        )
        
        if 'Item' in response:
            item = response['Item']
            return {
                'username': item['username']['S'],
                'temp_password': item['temp_password']['S']
            }
        else:
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_professor_credentials():
    """Get professor credentials from DynamoDB table"""
    dynamodb = boto3.client('dynamodb')
    
    try:
        response = dynamodb.get_item(
            TableName='iesb-student-credentials',
            Key={'username': {'S': 'professor'}}
        )
        
        if 'Item' in response:
            item = response['Item']
            return {
                'username': item['username']['S'],
                'temp_password': item['temp_password']['S']
            }
        else:
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_credentials_via_sns(cred, account_id, topic_arn):
    """Send credentials and student links via SNS"""
    confirm = input(f"Send SNS message for {cred['username']}? (y/N): ").strip().lower()
    if confirm != 'y':
        print("SNS message skipped")
        return False
        
    sns = boto3.client('sns')
    
    message = f"""Username: {cred['username']}
Password: {cred['temp_password']}
Account: {account_id}
Region: us-east-1
Console: https://{account_id}.signin.aws.amazon.com/console?region=us-east-1
{get_student_links(account_id)}"""
    
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=f"AWS Credentials for {cred['username']}"
        )
        print(f"SNS message sent successfully. MessageId: {response['MessageId']}")
        return True
    except Exception as e:
        print(f"Error sending SNS message: {e}")
        return False

def get_student_links(account_id):
    """Get student links formatted for SNS"""
    region = "us-east-1"
    
    links = f"""
AWS BIGDATA CLASS - STUDENT LINKS
Account ID: {account_id}
Region: {region}
Console: https://{account_id}.signin.aws.amazon.com/console?region={region}

GLUE:
Jobs: https://{region}.console.aws.amazon.com/glue/home#etl:tab=jobs
Crawlers: https://{region}.console.aws.amazon.com/glue/home#catalog:tab=crawlers
Databases: https://{region}.console.aws.amazon.com/glue/home#catalog:tab=databases

ATHENA:
Query Editor: https://{region}.console.aws.amazon.com/athena/home#/query-editor

S3:
Class Bucket: https://{region}.console.aws.amazon.com/s3/buckets/iesb-bigdata/

PERFORMANCE INSIGHTS:
RDS PI: https://{region}.console.aws.amazon.com/rds/home#performance-insights-v20206:
"""
    return links

def print_credentials(cred, account_id):
    """Print credentials with console link"""
    console_url = f"https://{account_id}.signin.aws.amazon.com/console?region=us-east-1"
    
    print(f"Username: {cred['username']}")
    print(f"Password: {cred['temp_password']}")
    print(f"Account: {account_id}")
    print(f"Region: us-east-1")
    print(f"Console: {console_url}")

def main():
    account_id = get_account_id()
    
    # Check for SNS topic ARN argument
    sns_topic_arn = None
    if len(sys.argv) > 2 and sys.argv[-1].startswith('arn:aws:sns:'):
        sns_topic_arn = sys.argv[-1]
        sys.argv = sys.argv[:-1]  # Remove SNS ARN from args for normal processing
    
    # Print student links once at the beginning
    print(get_student_links(account_id))
    print("=" * 60)
    
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "0"):
        # No arguments or "0" argument - print all credentials
        creds = get_all_credentials()
        if creds:
            for cred in creds:
                print_credentials(cred, account_id)
                if sns_topic_arn:
                    send_credentials_via_sns(cred, account_id, sns_topic_arn)
                print("-" * 60)
        else:
            print("No credentials found")
    elif len(sys.argv) == 2:
        # Single username argument
        username = sys.argv[1]
        
        if username == "professor":
            creds = get_user_credentials("professor-BigData")
        else:
            creds = get_user_credentials(username)
        
        if creds:
            print_credentials(creds, account_id)
            if sns_topic_arn:
                send_credentials_via_sns(creds, account_id, sns_topic_arn)
        else:
            print(f"User {username} not found")
    else:
        print("Usage: python get_user_creds.py [username|professor|0] [sns_topic_arn]")
        print("  No arguments or 0: Print all credentials")
        print("  With username: Print specific user credentials")
        print("  With professor: Print professor credentials")
        print("  Optional SNS topic ARN: Send credentials via SNS")
        print("Example: python get_user_creds.py aluno-BigData-1")
        print("Example: python get_user_creds.py professor")
        print("Example: python get_user_creds.py aluno-BigData-1 arn:aws:sns:us-east-1:123456789012:student-creds")
        sys.exit(1)

if __name__ == "__main__":
    main()
