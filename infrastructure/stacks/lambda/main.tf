resource "aws_lambda_function" "road_distance_lambda" {
  function_name = "${var.service_prefix}-rd-lambda"
  role          = aws_iam_role.road_distance_lambda_role.arn
  publish       = true
  package_type  = "Image"
  timeout       = "30"
  image_uri     = "${var.aws_lambda_ecr}/${var.project_group_short}/${var.project_name_short}/roaddistance-lambda:${var.image_version}"
  tracing_config {
    mode = "Active"
  }
  environment {
    variables = {
      "DRD_BASICAUTH" = "Basic ${var.drd_basicauth}"
      "DRD_ENDPOINT"  = var.drd_endpoint
      "DRD_MOCK_MODE" = var.drd_mock
    }
  }
  depends_on = [
    aws_iam_role.road_distance_lambda_role,
    aws_iam_role_policy.road_distance_lambda_role_policy,
    aws_cloudwatch_log_group.road_distance_lambda_log_group
  ]
}

resource "aws_lambda_function_event_invoke_config" "road_distance_lambda_invoke_config" {
  function_name          = aws_lambda_function.road_distance_lambda.function_name
  maximum_retry_attempts = 0
}

resource "aws_iam_role" "road_distance_lambda_role" {
  name               = "${var.service_prefix}-rd-role"
  path               = "/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "road_distance_lambda_role_policy" {
  name   = "${var.service_prefix}-rd-role-policy"
  role   = aws_iam_role.road_distance_lambda_role.name
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "xray:PutTraceSegments",
        "xray:PutTelemetryRecords",
        "xray:GetSamplingRules",
        "xray:GetSamplingTargets",
        "xray:GetSamplingStatisticSummaries"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
POLICY
}

resource "aws_cloudwatch_log_group" "road_distance_lambda_log_group" {
  name              = "/aws/lambda/${var.service_prefix}-rd-lambda"
  retention_in_days = "0"
}

resource "aws_lambda_function" "auth_lambda" {
  function_name = "${var.service_prefix}-auth-lambda"
  role          = aws_iam_role.auth_lambda_role.arn
  publish       = true
  package_type  = "Image"
  timeout       = "30"
  image_uri     = "${var.aws_lambda_ecr}/${var.project_group_short}/${var.project_name_short}/authoriser-lambda:${var.image_version}"
  tracing_config {
    mode = "Active"
  }
  environment {
    variables = {
      "SECRET_STORE" = var.deployment_secrets
    }
  }
  depends_on = [
    aws_iam_role.auth_lambda_role,
    aws_iam_role_policy.auth_lambda_role_policy,
    aws_cloudwatch_log_group.auth_lambda_log_group
  ]
}

resource "aws_lambda_function_event_invoke_config" "auth_lambda_invoke_config" {
  function_name          = aws_lambda_function.auth_lambda.function_name
  maximum_retry_attempts = 0
}

resource "aws_iam_role" "auth_lambda_role" {
  name               = "${var.service_prefix}-auth-role"
  path               = "/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "auth_lambda_role_policy" {
  name   = "${var.service_prefix}-auth-role-policy"
  role   = aws_iam_role.auth_lambda_role.name
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:Describe*",
        "secretsmanager:Get*",
        "secretsmanager:List*"
      ],
      "Resource": [
        "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account_id}:secret:${var.project_group_short}*",
        "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account_id}:secret:core-dos*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "xray:PutTraceSegments",
        "xray:PutTelemetryRecords",
        "xray:GetSamplingRules",
        "xray:GetSamplingTargets",
        "xray:GetSamplingStatisticSummaries"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
POLICY
}

resource "aws_cloudwatch_log_group" "auth_lambda_log_group" {
  name              = "/aws/lambda/${var.service_prefix}-auth-lambda"
  retention_in_days = "0"
}
