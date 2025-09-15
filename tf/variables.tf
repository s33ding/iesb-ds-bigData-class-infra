variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "student_count" {
  description = "Number of student users to create"
  type        = number
  default     = 18
}
