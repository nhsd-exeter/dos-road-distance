data "terraform_remote_state" "api_gateway" {
  backend = "s3"
  config = {
    bucket = var.texas_terraform_state_store
    key    = var.api_gateway_tf_state_key
    region = var.aws_region
  }
}
