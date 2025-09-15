resource "aws_athena_workgroup" "bigdata" {
  name = "bigdata-workgroup"

  configuration {
    enforce_workgroup_configuration = true
    result_configuration {
      output_location = "s3://iesb-bigdata/athena-results/"
    }
  }
}

resource "aws_athena_database" "bigdata" {
  name   = "bigdata_db"
  bucket = "iesb-bigdata"
}
