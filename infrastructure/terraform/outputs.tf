output "class_bucket_name" {
  value = aws_s3_bucket.class_bucket.bucket
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.credentials.name
}

output "glue_job_name" {
  value = "Replaced with shared notebook"
}

output "student_usernames" {
  value = aws_iam_user.students[*].name
}

output "teacher_username" {
  value = aws_iam_user.teacher.name
}

output "teacher_password" {
  value     = aws_iam_user_login_profile.teacher.password
  sensitive = true
}

output "glue_connection" {
  value = aws_glue_connection.rds_connection.name
}

output "sns_topic_arn" {
  description = "SNS topic ARN for credentials notifications"
  value       = aws_sns_topic.student_credentials.arn
}
