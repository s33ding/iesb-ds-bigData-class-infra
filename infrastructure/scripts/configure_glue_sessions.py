#!/usr/bin/env python3
import boto3

def configure_student_glue_access():
    """Configure Glue access for all students"""
    iam = boto3.client('iam')
    
    # Glue policy for students
    glue_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "glue:*",
                    "iam:PassRole"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::iesb-bigdata/*",
                    "arn:aws:s3:::iesb-bigdata"
                ]
            }
        ]
    }
    
    # Create or update policy
    policy_name = "IESBStudentGlueAccess"
    try:
        iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=str(glue_policy).replace("'", '"'),
            Description="Glue access for IESB students"
        )
        print(f"Created policy: {policy_name}")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"Policy {policy_name} already exists")
    
    # Attach to all students
    for i in range(1, 19):
        username = f"aluno-BigData-{i}"
        try:
            iam.attach_user_policy(
                UserName=username,
                PolicyArn=f"arn:aws:iam::248189947068:policy/{policy_name}"
            )
            print(f"Attached Glue policy to {username}")
        except Exception as e:
            print(f"Error attaching policy to {username}: {e}")

if __name__ == "__main__":
    configure_student_glue_access()
