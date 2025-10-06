# Upload DAG to existing Airflow S3 bucket
# resource "aws_s3_object" "bronze_dag" {
#   bucket = "dataiesb-airflow"
#   key    = "dags/bronze_layer_etl.py"
#   source = "${path.module}/../airflow/dags/bronze_layer_etl.py"
#   etag   = filemd5("${path.module}/../airflow/dags/bronze_layer_etl.py")
# }

# Upload bronze layer ETL script
# resource "aws_s3_object" "bronze_etl_script" {
#   bucket = aws_s3_bucket.class_bucket.id
#   key    = "scripts/bronze-layer-etl.py"
#   source = "${path.module}/../glue-examples/bronze-layer-etl.py"
#   etag   = filemd5("${path.module}/../glue-examples/bronze-layer-etl.py")
# }

# Upload crawler trigger script
# resource "aws_s3_object" "crawler_trigger_script" {
#   bucket = aws_s3_bucket.class_bucket.id
#   key    = "scripts/trigger_crawler.py"
#   source = "${path.module}/../airflow/scripts/trigger_crawler.py"
#   etag   = filemd5("${path.module}/../airflow/scripts/trigger_crawler.py")
# }
