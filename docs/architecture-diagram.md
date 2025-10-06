# IESB Big Data Infrastructure - Architecture Overview

## System Architecture Diagram

```mermaid
graph TB
    %% Student Access
    Student[👨‍🎓 Student] --> TempCreds[🔑 Temporary Credentials]
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

## Data Lake Methodology: Bronze, Silver, Gold Layers

### 🥉 Bronze Layer (Raw Data)
- **Purpose**: Store raw, unprocessed data exactly as extracted from source
- **Format**: Original format from RDS (JSON, Parquet, etc.)
- **Schema**: Minimal or no schema enforcement
- **Use Case**: Data archival, reprocessing, audit trail

### 🥈 Silver Layer (Cleaned Data)
- **Purpose**: Cleaned, validated, and standardized data
- **Format**: Optimized formats (Parquet, Delta)
- **Schema**: Enforced schema with data quality rules
- **Use Case**: Data science, feature engineering, reporting

### 🥇 Gold Layer (Analytics Ready)
- **Purpose**: Business-ready, aggregated data for analytics
- **Format**: Highly optimized for query performance
- **Schema**: Star/snowflake schema, dimensional modeling
- **Use Case**: BI dashboards, executive reporting, ML models

## Student Workflow

1. **Access**: Login with temporary credentials → Force password reset
2. **Development**: Upload Glue notebooks → Connect to RDS via JDBC
3. **Extraction**: Extract tables → Monitor with Performance Insights
4. **Processing**: Save to Bronze layer → Run Glue Crawlers
5. **Transformation**: Process Bronze → Silver → Gold layers
6. **Analytics**: Query with Athena → Create views → Explore data lake patterns

## Key Learning Objectives

- **Data Lake Architecture**: Understanding layered approach to data storage
- **ETL/ELT Processes**: Hands-on experience with AWS Glue
- **Data Cataloging**: Automatic schema discovery with Glue Crawlers
- **Analytics**: SQL querying with Athena across different data layers
- **Performance Monitoring**: Database performance analysis with RDS Performance Insights
