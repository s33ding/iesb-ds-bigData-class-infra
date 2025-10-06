resource "aws_s3_bucket" "class_bucket" {
  bucket = var.class_bucket_name
  
  tags = {
    Name = "IESB BigData Class Bucket"
  }
}

# S3 objects for folder structure
resource "aws_s3_object" "bronze_folder" {
  bucket = aws_s3_bucket.class_bucket.id
  key    = "bronze/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "athena_results_folder" {
  bucket = aws_s3_bucket.class_bucket.id
  key    = "athena-results/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "scripts_folder" {
  bucket = aws_s3_bucket.class_bucket.id
  key    = "scripts/"
  content_type = "application/x-directory"
}

# Sysadmin bucket for credentials export
resource "aws_s3_bucket" "sysadmin_bucket" {
  bucket = "dataiesb-sysadmin"
  
  tags = {
    Name = "IESB Sysadmin Bucket"
  }
}

resource "aws_s3_bucket_public_access_block" "sysadmin_bucket" {
  bucket = aws_s3_bucket.sysadmin_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Execute credentials export script
resource "null_resource" "export_credentials" {
  depends_on = [
    aws_dynamodb_table_item.student_credentials,
    aws_s3_bucket.sysadmin_bucket,
    aws_sns_topic.student_credentials
  ]

  provisioner "local-exec" {
    command = "python3 export_credentials.py"
    working_dir = path.module
  }

  triggers = {
    student_count = var.student_count
    sns_topic_arn = aws_sns_topic.student_credentials.arn
  }
}

# Invalidate user sessions when credentials are destroyed
resource "null_resource" "invalidate_sessions" {
  depends_on = [aws_iam_user.students, aws_iam_user.teacher]

  provisioner "local-exec" {
    when    = destroy
    command = "python3 ../scripts/invalidate_sessions.py"
    working_dir = path.module
  }

  triggers = {
    student_count = var.student_count
  }
}
