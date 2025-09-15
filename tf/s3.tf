resource "aws_s3_bucket" "class_bucket" {
  bucket = "iesb-bigdata"
  
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
