resource "aws_dynamodb_table" "credentials" {
  name           = "iesb-student-credentials"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "username"

  attribute {
    name = "username"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.credentials.arn
  }
}

resource "aws_kms_key" "credentials" {
  description = "KMS key for student credentials table"
}

resource "aws_dynamodb_table_item" "student_credentials" {
  count      = var.student_count
  table_name = aws_dynamodb_table.credentials.name
  hash_key   = aws_dynamodb_table.credentials.hash_key

  item = jsonencode({
    username = {
      S = aws_iam_user.students[count.index].name
    }
    temp_password = {
      S = aws_iam_user_login_profile.students[count.index].password
    }
  })
}
