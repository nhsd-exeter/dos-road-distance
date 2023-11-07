data "aws_iam_policy_document" "iam_policy" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${var.service_prefix}-performance/*",
      "arn:aws:s3:::${var.service_prefix}-performance"
    ]
  }
}

