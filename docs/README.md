# IESB Big Data Infrastructure Documentation

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

## Getting Started

1. Review the main README.md in the root directory
2. Check infrastructure/terraform/ for AWS resource configurations
3. Explore examples/notebooks/ for hands-on tutorials
4. Run tests from testing/ directories to validate setup

## Components

- **Infrastructure**: Terraform modules for AWS resources (S3, Glue, Athena, etc.)
- **Scripts**: Automation scripts for user management and configuration
- **Examples**: Educational notebooks and code samples
- **Testing**: Comprehensive test suite for infrastructure validation
- **Deployment**: Production deployment configurations
