resource "aws_iam_user" "teacher" {
  name          = "professor-BigData"
  force_destroy = true
}

resource "aws_iam_user_group_membership" "teacher" {
  user   = aws_iam_user.teacher.name
  groups = [aws_iam_group.students.name]
}

resource "aws_iam_user_login_profile" "teacher" {
  user                    = aws_iam_user.teacher.name
  password_reset_required = true
}

resource "aws_iam_group" "students" {
  name = "iesb-bigdata-students"
}

resource "aws_iam_user" "students" {
  count = var.student_count
  name  = "aluno-BigData-${count.index + 1}"
  force_destroy = true
}

resource "aws_iam_user_group_membership" "students" {
  count = var.student_count
  user  = aws_iam_user.students[count.index].name
  groups = [aws_iam_group.students.name]
}

resource "aws_iam_user_login_profile" "students" {
  count   = var.student_count
  user    = aws_iam_user.students[count.index].name
  password_reset_required = true
}

resource "aws_iam_group_policy" "glue_access" {
  name  = "glue-access"
  group = aws_iam_group.students.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "glue:*"
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = "s3:*"
        Resource = [
          aws_s3_bucket.class_bucket.arn,
          "${aws_s3_bucket.class_bucket.arn}/*",
          "arn:aws:s3:::aws-glue-assets-*",
          "arn:aws:s3:::aws-glue-assets-*/*",
          "arn:aws:s3:::dataiesb-airflow",
          "arn:aws:s3:::dataiesb-airflow/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:CreateBucket",
          "s3:ListAllMyBuckets",
          "s3:ListBucket"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:ListRoles",
          "iam:GetRole",
          "iam:PassRole"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "athena:*",
          "lakeformation:*",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "airflow:*"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "pi:DescribeDimensionKeys",
          "pi:GetDimensionKeyDetails",
          "pi:GetResourceMetadata",
          "pi:GetResourceMetrics",
          "pi:ListAvailableResourceDimensions",
          "pi:ListAvailableResourceMetrics"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "rds:DescribeDBInstances",
          "rds:DescribeDBClusters",
          "rds:DescribeGlobalClusters"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:ListMetrics",
          "cloudwatch:GetMetricStatistics"
        ]
        Resource = "*"
      }
    ]
  })
}

# Metabase IAM role for EKS service account (IRSA)
resource "aws_iam_role" "metabase_role" {
  name = "metabase-athena-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/oidc.eks.sa-east-1.amazonaws.com/id/YOUR_EKS_OIDC_ID"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "oidc.eks.sa-east-1.amazonaws.com/id/YOUR_EKS_OIDC_ID:sub" = "system:serviceaccount:default:metabase-service-account"
            "oidc.eks.sa-east-1.amazonaws.com/id/YOUR_EKS_OIDC_ID:aud" = "sts.amazonaws.com"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "metabase_athena" {
  name = "metabase-athena-policy"
  role = aws_iam_role.metabase_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "athena:*",
          "glue:GetDatabase",
          "glue:GetDatabases", 
          "glue:GetTable",
          "glue:GetTables",
          "glue:GetPartition",
          "glue:GetPartitions"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          aws_s3_bucket.class_bucket.arn,
          "${aws_s3_bucket.class_bucket.arn}/*"
        ]
      }
    ]
  })
}

data "aws_caller_identity" "current" {}

resource "aws_iam_group_policy" "password_change" {
  name  = "password-change"
  group = aws_iam_group.students.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iam:ChangePassword",
          "iam:GetUser"
        ]
        Resource = "arn:aws:iam::*:user/$${aws:username}"
      }
    ]
  })
}
