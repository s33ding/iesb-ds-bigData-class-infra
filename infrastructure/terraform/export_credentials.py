#!/usr/bin/env python3
import boto3
import json
import os
import sys
from datetime import datetime

def export_credentials(send_sns=True):
    # Initialize AWS clients
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    sts = boto3.client('sts')
    
    # Get account ID
    account_id = sts.get_caller_identity()['Account']
    
    # Get table
    table = dynamodb.Table('iesb-student-credentials')
    
    # Scan all items
    response = table.scan()
    items = response['Items']
    
    # Handle pagination if needed
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    
    # Create export data
    export_data = {
        'export_timestamp': datetime.utcnow().isoformat(),
        'total_records': len(items),
        'account_id': account_id,
        'region': 'us-east-1',
        'console_url': f'https://{account_id}.signin.aws.amazon.com/console?region=us-east-1',
        'credentials': items
    }
    
    # Write to temp file
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    temp_file = f'/tmp/credentials-export-{timestamp}.json'
    with open(temp_file, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    # Upload to sysadmin bucket
    s3.upload_file(
        temp_file,
        'dataiesb-sysadmin',
        f'credentials-export-{timestamp}.json'
    )
    
    # Send SNS notification only if requested
    if send_sns:
        message = f"""BigData Class Credentials Export Complete

Export Details:
- Timestamp: {export_data['export_timestamp']}
- Total Students: {len(items)}
- Account ID: {account_id}
- Region: us-east-1
- Console URL: {export_data['console_url']}

Credentials file uploaded to: s3://dataiesb-sysadmin/credentials-export-{timestamp}.json

Student Credentials Summary:
"""
        
        # Add credential summary to message
        for item in sorted(items, key=lambda x: x['username']):
            message += f"\nUsername: {item['username']}\nPassword: {item['temp_password']}\n"
        
        try:
            sns.publish(
                TopicArn=f'arn:aws:sns:us-east-1:{account_id}:bigdata-students-cred',
                Subject='BigData Class - Student Credentials Export',
                Message=message
            )
            print(f"SNS notification sent to teachers")
        except Exception as e:
            print(f"Failed to send SNS notification: {e}")
    else:
        print("SNS notification skipped")
    
    # Clean up temp file
    os.remove(temp_file)
    
    # Print credentials in requested format
    print(f"Exported {len(items)} credentials to dataiesb-sysadmin bucket")
    print("\nCredentials:")
    print("-" * 60)
    
    for item in sorted(items, key=lambda x: x['username']):
        print(f"Username: {item['username']}")
        print(f"Password: {item['temp_password']}")
        print(f"Account: {account_id}")
        print(f"Region: us-east-1")
        print(f"Console: https://{account_id}.signin.aws.amazon.com/console?region=us-east-1")
        print("-" * 60)

if __name__ == "__main__":
    # Check for any argument to disable SNS sending
    send_sns = len(sys.argv) == 1  # Only send SNS if no arguments provided
    
    export_credentials(send_sns)
