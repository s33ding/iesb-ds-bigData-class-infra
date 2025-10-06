# Simple Data Flow Overview

## Student Journey: From RDS to Analytics

```
👨‍🎓 Student Login (Temp Creds) 
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

## Data Lake Layers

| Layer | Purpose | Format | Use Case |
|-------|---------|--------|----------|
| 🥉 Bronze | Raw data storage | Original format | Archive, reprocess |
| 🥈 Silver | Cleaned & validated | Parquet/Delta | Data science, reports |
| 🥇 Gold | Business ready | Optimized schema | BI, ML, analytics |

## AWS Services Used

- **IAM**: Student access management
- **RDS**: Source database with Performance Insights
- **Glue**: ETL jobs, crawlers, data catalog
- **S3**: Data lake storage (Bronze/Silver/Gold)
- **Athena**: Serverless SQL analytics
- **DynamoDB**: Credential storage
