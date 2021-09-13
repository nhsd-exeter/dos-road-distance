data "terraform_remote_state" "lambda" {
  backend = "s3"
  config = {
    bucket = var.texas_terraform_state_store
    key    = var.lambda_tf_state_key
    region = var.aws_region
  }
}
