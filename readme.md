# IESB Big Data Infrastructure

This repository contains the infrastructure code for the IESB Big Data class, including Terraform configurations for AWS services and supporting scripts.

## Architecture Overview

### System Architecture Diagram

```mermaid
graph TB
    %% Student Access
    Student[👨🎓 Student] --> TempCreds[🔑 Temporary Credentials]
    TempCreds --> Console[🖥️ AWS Console Access]
    
    %% Data Source
    Console --> RDS[(🗄️ Amazon RDS)]
    RDS --> PI[📈 Performance Insights]
    
    %% Secrets Manager
    SecretsManager[🔐 AWS Secrets Manager<br/>RDS Credentials]
    
    %% Glue Ecosystem
    subgraph GlueEco["🔧 AWS Glue Ecosystem"]
        GlueCatalog[📊 Data Catalog]
        GlueNotebook[📓 Interactive Sessions]
        subgraph SparkJupyter["⚡ Spark/Jupyter"]
            GlueExamples[📝 Glue Examples/Spark Jobs]
            JDBC[🔌 JDBC Connection]
        end
        Crawler1[🕷️ Crawler Bronze]
        Crawler2[🕷️ Crawler Silver] 
        Transform1[⚡ Spark ETL Bronze→Silver]
    end
    
    %% S3 Data Lake
    subgraph S3Lake["🗄️ S3 Data Lake"]
        S3Bronze[🥉 Bronze Layer<br/>Raw Data]
        S3Silver[🥈 Silver Layer<br/>Cleaned Data]
        S3Gold[🥇 Gold Layer<br/>Analytics Ready]
    end
    
    Console --> GlueEco
    SecretsManager --> JDBC
    JDBC --> RDS
    
    %% Data Flow
    GlueExamples --> S3Bronze
    S3Bronze --> Crawler1
    Crawler1 --> GlueCatalog
    Crawler1 --> Athena[🔍 Amazon Athena]
    
    Transform1 --> S3Silver
    S3Silver --> Crawler2
    Crawler2 --> GlueCatalog
    
    %% Analytics
    Athena --> Views[👁️ Create Views]
    Athena --> Queries[📊 SQL Queries]
    
    %% Styling
    classDef student fill:#e1f5fe
    classDef aws fill:#ff9800
    classDef storage fill:#4caf50
    classDef analytics fill:#9c27b0
    classDef glue fill:#2196f3
    
    class Student,TempCreds,Console student
    class RDS,PI,SecretsManager aws
    class S3Lake,S3Bronze,S3Silver,S3Gold storage
    class Athena,Views,Queries analytics
    class GlueEco,GlueCatalog,GlueNotebook,SparkJupyter,GlueExamples,JDBC,Crawler1,Crawler2,Transform1 glue
```

### Simple Data Flow

```
👨🎓 Student Login (Temp Creds) 
    ↓
🖥️ AWS Console Access
    ↓
┌─────────────────────────────────┐
│     🔧 AWS Glue Ecosystem       │
│  📓 Interactive Sessions        │
│  ┌─────────────────────────────┐ │
│  │   ⚡ Spark/Jupyter          │ │
│  │ 📝 Spark Jobs/Examples      │ │
│  │ 🔌 JDBC Connection          │ │
│  └─────────────────────────────┘ │
│  🕷️ Crawlers (Bronze/Silver)    │
│  📊 Data Catalog               │
│  ⚡ Spark ETL Transformations   │
└─────────────────────────────────┘
    ↓
🔐 Secrets Manager (RDS Creds) → 🗄️ RDS → 📈 Performance Insights
    ↓
┌─────────────────────────────────┐
│        🗄️ S3 Data Lake          │
│  🥉 Bronze Layer (Raw Data)     │
│  🥈 Silver Layer (Clean Data)   │
│  🥇 Gold Layer (Analytics Ready)│
└─────────────────────────────────┘
    ↓ 
🔍 Athena Queries & Views
```

### Data Lake Layers

| Layer | Purpose | Format | Use Case |
|-------|---------|--------|----------|
| 🥉 Bronze | Raw data storage | Original format | Archive, reprocess |
| 🥈 Silver | Cleaned & validated | Parquet/Delta | Data science, reports |
| 🥇 Gold | Business ready | Optimized schema | BI, ML, analytics |

## Project Structure

```
├── docs/                    # Documentation
├── infrastructure/          # Infrastructure as Code
│   ├── terraform/          # Terraform configurations
│   └── scripts/            # Infrastructure management scripts
├── examples/               # Code examples and tutorials
│   ├── glue/              # AWS Glue examples
│   └── notebooks/         # Jupyter notebooks
├── testing/               # Test suites
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
└── deployment/            # Deployment configurations
    ├── airflow/           # Apache Airflow setup
    └── metabase/          # Metabase deployment
```

## What This Infrastructure Creates

### IAM
- 18 student users created dynamically and added to a new IAM Group
- Console access with temporary passwords (force reset on first login)
- Programmatic access (optional) via access keys
- Group policies granting full access to the Glue ecosystem and class S3 bucket

### DynamoDB
- Table to store initial login materials (username, temp console password, optional access keys)
- SSE-KMS encrypted, with least-privilege write access from Terraform only

### S3
- One class bucket (e.g., iesb-bigdata-<suffix>) that the student group can fully access

### Glue
- Glue job (Spark) that reads from Amazon RDS using Secrets Manager secret (rds-secret)
- Writes output to the S3 bucket
- Glue service role with access to the secret, class bucket, CloudWatch logs, and Glue resources

## Prerequisites

- AWS CLI configured
- Terraform installed
- Python 3.x with required packages (see requirements.txt)

## Quick Start

1. Configure your AWS credentials
2. Update `infrastructure/terraform/terraform.tfvars` with your specific values
3. Run `terraform init` and `terraform apply` in the `infrastructure/terraform/` directory
4. Use scripts in `infrastructure/scripts/` directory for user management

## Testing

- Unit tests: `cd testing/unit && python run_tests.py`
- Integration tests: Run tests from `testing/integration/` directory

## Documentation

See `docs/` directory for detailed documentation and guides.

## Security Note

⚠️ Storing plaintext temp passwords in DynamoDB is inherently sensitive. This setup:
- Forces password reset at first login
- Encrypts the table with KMS
- Limits who can read the table (by default, only admins)

Prefer distributing credentials over secure channels and deleting rows after students log in.
