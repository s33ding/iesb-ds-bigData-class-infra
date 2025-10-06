resource "aws_iam_role" "glue_service" {
  name = "iesb-glue-service-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "glue_service" {
  name = "glue-service-policy"
  role = aws_iam_role.glue_service.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          "arn:aws:secretsmanager:${var.aws_region}:*:secret:${var.rds_read_only_secret_name}*"
        ]
      },
      {
        Effect = "Allow"
        Action = "s3:*"
        Resource = [
          aws_s3_bucket.class_bucket.arn,
          "${aws_s3_bucket.class_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = "glue:*"
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = "iam:PassRole"
        Resource = aws_iam_role.glue_service.arn
      },
      {
        Effect = "Allow"
        Action = [
          "codewhisperer:GenerateRecommendations",
          "codewhisperer:GetRecommendations"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeSubnets",
          "ec2:DescribeVpcs",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeAvailabilityZones",
          "ec2:CreateNetworkInterface",
          "ec2:DeleteNetworkInterface"
        ]
        Resource = "*"
      }
    ]
  })
}



data "aws_secretsmanager_secret" "rds_secret" {
  name = var.rds_read_only_secret_name
}

data "aws_secretsmanager_secret_version" "rds_secret" {
  secret_id = data.aws_secretsmanager_secret.rds_secret.id
}

resource "aws_glue_connection" "rds_connection" {
  name = "iesb-rds-connection"
  
  connection_properties = {
    JDBC_CONNECTION_URL = "jdbc:postgresql://${jsondecode(data.aws_secretsmanager_secret_version.rds_secret.secret_string)["host"]}:5432/${jsondecode(data.aws_secretsmanager_secret_version.rds_secret.secret_string)["dbname"]}"
    USERNAME = jsondecode(data.aws_secretsmanager_secret_version.rds_secret.secret_string)["username"]
    PASSWORD = jsondecode(data.aws_secretsmanager_secret_version.rds_secret.secret_string)["password"]
  }
  
  physical_connection_requirements {
    availability_zone      = "us-east-1b"
    security_group_id_list = [aws_security_group.glue_connection.id]
    subnet_id             = data.aws_subnets.prod.ids[0]
  }

  tags = {
    Name = "IESB BigData Class PostgreSQL Connection"
    Role = aws_iam_role.glue_service.arn
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

# Glue Database
resource "aws_glue_catalog_database" "iesb_database" {
  name = "iesb"
  description = "IESB BigData class database"
}

# S3 Crawler
resource "aws_glue_crawler" "s3_crawler" {
  database_name = aws_glue_catalog_database.iesb_database.name
  name          = "iesb-s3-crawler"
  role          = aws_iam_role.glue_service.arn

  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/censo_escolar_2024/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/ed_enem_2024_participantes/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/ed_enem_2024_resultados/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/ed_enem_2024_resultados_amos_per/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/ed_superior_cursos/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/ed_superior_ies/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/educacao_basica/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/municipio/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/municipio_ride_brasilia/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/ocorrencia/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/pib_municipios/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/regiao/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/sus_aih/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/sus_procedimento_ambulatorial/"
  }
  
  s3_target {
    path = "s3://${aws_s3_bucket.class_bucket.bucket}/bronze/unidade_federacao/"
  }

  configuration = jsonencode({
    "Version" = 1.0
    "CrawlerOutput" = {
      "Partitions" = {
        "AddOrUpdateBehavior" = "InheritFromTable"
      }
      "Tables" = {
        "AddOrUpdateBehavior" = "MergeNewColumns"
      }
    }
  })

  tags = {
    Name = "IESB S3 Crawler"
  }
}

# RDS Crawler
resource "aws_glue_crawler" "rds_crawler" {
  database_name = aws_glue_catalog_database.iesb_database.name
  name          = "iesb-rds-crawler"
  role          = aws_iam_role.glue_service.arn

  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/municipio"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/unidade_federacao"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/regiao"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/ed_enem_2024_resultados"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/ed_enem_2024_participantes"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/educacao_basica"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/censo_escolar_2024"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/pib_municipios"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/sus_aih"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/sus_procedimento_ambulatorial"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/ed_superior_cursos"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/ed_superior_ies"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/agregados_setores_censitarios"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/Censo_20222_Populacao_Idade_Sexo"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/municipio_ride_brasilia"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/ocorrencia"
  }
  
  jdbc_target {
    connection_name = aws_glue_connection.rds_connection.name
    path            = "iesb/ed_enem_2024_resultados_amos_per"
  }

  configuration = jsonencode({
    "Version" = 1.0
    "CrawlerOutput" = {
      "Tables" = {
        "AddOrUpdateBehavior" = "MergeNewColumns"
      }
    }
  })

  tags = {
    Name = "IESB RDS Crawler"
  }
}

data "aws_subnets" "prod" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.prod.id]
  }
}

resource "aws_security_group" "glue_connection" {
  name_prefix = "glue-connection-"
  vpc_id      = data.aws_vpc.prod.id
  
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    self      = true
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


