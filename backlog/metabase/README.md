# Metabase Deployment for IESB BigData Class

This directory contains Kubernetes manifests to deploy Metabase on EKS in sa-east-1 region with Athena connectivity.

## Files

- `deployment.yaml` - Metabase deployment, service, and PVC
- `ingress.yaml` - ALB Ingress configuration
- `athena-config.yaml` - Athena connection configuration
- `deploy.sh` - Deployment script

## Deployment

1. Configure kubectl for EKS sa-east-1:
```bash
aws eks update-kubeconfig --region sa-east-1 --name your-cluster-name
```

2. Deploy Metabase:
```bash
./deploy.sh
```

## Access

- URL: https://metabase.dataiesb.com
- The ALB will be automatically created via the ingress

## Athena Connection

Metabase will connect to Athena with these settings:
- **Region**: us-east-1
- **Workgroup**: primary
- **S3 Staging**: s3://iesb-bigdata/athena-results/
- **Catalog**: AwsDataCatalog
- **Schema**: iesb_bigdata_db

## Data Sources

Students can query the bronze layer tables:
- Geographic data (municipio, unidade_federacao, regiao)
- Education data (ENEM results, school census)
- Health data (SUS procedures)
- Demographics and economics data

## Notes

- Uses IAM roles for Athena authentication
- Persistent storage for Metabase database
- SSL termination at ALB level
- Health checks configured for ALB
