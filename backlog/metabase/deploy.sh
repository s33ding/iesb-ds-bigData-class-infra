#!/bin/bash

# Deploy Metabase to EKS sa-east-1
# Make sure kubectl is configured for the correct cluster

echo "Deploying Metabase to EKS sa-east-1..."

# Set context to sa-east-1 region
kubectl config use-context arn:aws:eks:sa-east-1:248189947068:cluster/your-cluster-name

# Apply configurations
echo "Creating Metabase deployment..."
kubectl apply -f deployment.yaml

echo "Creating Athena configuration..."
kubectl apply -f athena-config.yaml

echo "Creating ALB Ingress..."
kubectl apply -f ingress.yaml

# Wait for deployment
echo "Waiting for Metabase to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/metabase

# Get ALB URL
echo "Getting ALB URL..."
kubectl get ingress metabase-ingress

echo "Metabase deployment completed!"
echo "Access Metabase at: https://metabase.dataiesb.com"
echo ""
echo "Athena Connection Details:"
echo "- Region: us-east-1"
echo "- Workgroup: primary"
echo "- S3 Staging: s3://iesb-bigdata/athena-results/"
echo "- Catalog: AwsDataCatalog"
echo "- Schema: iesb_bigdata_db"
