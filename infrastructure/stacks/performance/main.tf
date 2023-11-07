module "performance_bucket" {
  source          = "../../modules/s3"
  bucket_name     = "${var.service_prefix}-performance"
  bucket_iam_role = "${var.service_prefix}-performance-bucket-role"
  attach_policy   = true
  log_bucket      = var.texas_s3_logs_bucket
  service_name    = var.project_group_short
  tags            = local.standard_tags
}
