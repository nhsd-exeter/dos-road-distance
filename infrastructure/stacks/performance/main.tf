resource "aws_iam_role" "iam_host_role" {
  path = "/"
  name = "${var.service_prefix}-performance-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement" : [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated" : "arn:aws:iam::${var.aws_account_id}:oidc-provider/${trimprefix(data.terraform_remote_state.eks.outputs.eks_oidc_issuer_url, "https://")}"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringLike": {
            "${trimprefix(data.terraform_remote_state.eks.outputs.eks_oidc_issuer_url, "https://")}:sub": "system:serviceaccount:${var.project_group_short}-${var.project_name_short}*:${var.service_prefix}-performance-sa"
        }
      }
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "iam_role_policy" {
  name   = "${var.service_prefix}-performance-role-policy"
  role   = aws_iam_role.iam_host_role.id
  policy = data.aws_iam_policy_document.iam_policy.json
}

module "performance_bucket" {
  source          = "../../modules/s3"
  bucket_name     = "${var.service_prefix}-performance"
  bucket_iam_role = "${var.service_prefix}-performance-bucket-role"
  attach_policy   = true
  log_bucket      = var.texas_s3_logs_bucket
  service_name    = var.project_group_short
  tags            = local.standard_tags
}
