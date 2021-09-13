resource "aws_lambda_function" "road_distance_lambda" {
  function_name = "${var.service_prefix}-rd-lambda"
  role          = aws_iam_role.road_distance_lambda_role.arn
  publish       = true
  package_type  = "Image"
  timeout       = "30"
  image_uri     = "${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.project_group_short}/${var.project_name_short}/road-distance:${var.image_version}"
  depends_on = [
    aws_iam_role.road_distance_lambda_role,
    aws_iam_role_policy.road_distance_lambda_role_policy,
    aws_cloudwatch_log_group.road_distance_lambda_log_group
  ]
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
    }
  ]
}
POLICY
}

resource "aws_cloudwatch_log_group" "road_distance_lambda_log_group" {
  name              = "/aws/lambda/${var.service_prefix}-rd-lambda"
  retention_in_days = "0"
}
