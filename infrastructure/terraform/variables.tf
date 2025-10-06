variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "student_count" {
  description = "Number of student users to create"
  type        = number
}

variable "class_bucket_name" {
  description = "Name of the main class S3 bucket"
  type        = string
}

variable "airflow_bucket_name" {
  description = "Name of the Airflow S3 bucket"
  type        = string
}

variable "glue_assets_bucket_prefix" {
  description = "Prefix for AWS Glue assets buckets"
  type        = string
}

variable "rds_read_only_secret_name" {
  description = "Name of the RDS read-only secret in AWS Secrets Manager"
  type        = string
  sensitive   = true
}

variable "favorite_aws_services" {
  description = "List of favorite AWS services for students to explore"
  type        = list(string)
  default = [
    "Glue (Jobs, Crawlers)",
    "S3",
    "Athena",
    "PI"
  ]
}
