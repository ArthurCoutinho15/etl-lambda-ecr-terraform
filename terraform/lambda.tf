resource "aws_lambda_function" "etl" {
  function_name = "etl-football"

  package_type = "Image"
  image_uri = "941377148408.dkr.ecr.us-east-1.amazonaws.com/arthur/etl-lambda@sha256:620cea093c839b32d370b2075fc3545df3e1527cf4aa76af149e080c7cc94559"

  role = aws_iam_role.lambda_role.arn

  memory_size = 1024
  timeout     = 30

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.data_lake.bucket
      API_TOKEN   = "xxxx"
    }
  }
}