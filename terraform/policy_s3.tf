resource "aws_iam_role_policy" "lambda_s3" {
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:PutObject"]
      Resource = "arn:aws:s3:::coutinho-lambda/*"
    }]
  })
}