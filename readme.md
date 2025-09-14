### IESB Big Data Class – Infrastructure (Terraform)

Provision IAM users, credentials storage, S3, Glue access, and a Glue job that extracts from RDS using Secrets Manager and writes to S3.

What this creates

IAM

18 student users created dynamically and added to a new IAM Group.

Console access with temporary passwords (force reset on first login).

Programmatic access (optional) via access keys.

Group policies granting full access to the Glue ecosystem and full access to a class S3 bucket.

DynamoDB

A new table to store initial login materials (username, temp console password, optional access keys).

SSE-KMS encrypted, with least-privilege write access from Terraform only.

S3

One class bucket (e.g., iesb-bigdata-<suffix>) that the student group can fully access.

Glue

A Glue job (Spark) that reads from Amazon RDS using an existing Secrets Manager secret (rds-secret), and writes output to the S3 bucket.

A Glue service role with access to the secret, the class bucket, CloudWatch logs, and Glue resources.

⚠️ Security note: Storing plaintext temp passwords in DynamoDB is inherently sensitive. This setup:

Forces password reset at first login.

Encrypts the table with KMS.

Limits who can read the table (by default, only admins).
Prefer distributing credentials over secure channels and deleting rows after students log in.
