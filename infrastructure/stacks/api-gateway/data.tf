data "terraform_remote_state" "lambda" {
  backend = "s3"
  config = {
    bucket = var.texas_terraform_state_store
    key    = var.lambda_tf_state_key
    region = var.aws_region
  }
}

data "aws_iam_policy_document" "apigateway_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["apigateway.amazonaws.com"]
    }
  }
}
