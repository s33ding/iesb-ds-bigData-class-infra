#!/usr/bin/env python3
import boto3
import sys

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

def main():
    if len(sys.argv) != 2:
        print("Usage: python get_user_creds.py <username>")
        print("Example: python get_user_creds.py aluno-BigData-1")
        sys.exit(1)
    
    username = sys.argv[1]
    creds = get_user_credentials(username)
    
    if creds:
        print(f"Username: {creds['username']}")
        print(f"Temp Password: {creds['temp_password']}")
    else:
        print(f"User {username} not found")

if __name__ == "__main__":
    main()
