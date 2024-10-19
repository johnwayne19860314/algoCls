provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "MyLambdaFunction"
  handler       = "lambda_function.lambda_handler" # The entry point in your code
  runtime       = "python3.8" # or your preferred runtime

  s3_bucket = "your-bucket-name" # Replace with your S3 bucket name where the zip file is stored
  s3_key    = "lambda.zip"        # The zip file containing your Lambda function code

  role = aws_iam_role.lambda_role.arn
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_api_gateway_rest_api" "my_api" {
  name        = "MyAPI"
  description = "My API Gateway for Lambda integration"
}

resource "aws_api_gateway_resource" "my_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "mylambda"
}

resource "aws_api_gateway_method" "my_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.my_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "my_integration" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.my_resource.id
  http_method = aws_api_gateway_method.my_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.my_lambda.invoke_arn
}
