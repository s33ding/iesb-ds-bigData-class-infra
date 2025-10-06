# SNS Topic for student credentials notifications
resource "aws_sns_topic" "student_credentials" {
  name = "bigdata-students-cred"
  
  tags = {
    Name = "BigData Students Credentials"
  }
}

# Email subscription for Alexandre
resource "aws_sns_topic_subscription" "alexandre_email" {
  topic_arn = aws_sns_topic.student_credentials.arn
  protocol  = "email"
  endpoint  = "alexandre.roriz@iesb.edu.br"
}

# Email subscription for Roberto
resource "aws_sns_topic_subscription" "roberto_email" {
  topic_arn = aws_sns_topic.student_credentials.arn
  protocol  = "email"
  endpoint  = "roberto.diniz@iesb.edu.br"
}
