############
# AWS COMMON
############

variable "aws_profile" {
  description = "The AWS profile"
}

variable "aws_region" {
  description = "The AWS region"
}

variable "aws_account_id" {
  description = "AWS account Number for Athena log location"
}

# ##############
# # TEXAS COMMON
# ##############

variable "profile" {
  description = "The tag used to identify profile e.g. dev, test, live, ..."
}

variable "terraform_platform_state_store" {
  description = "The Texas terraform state store bucket"
}

variable "eks_terraform_state_key" {
  description = "Location in s3 bucket of eks terraform state"
}

variable "texas_s3_logs_bucket" {
  description = "Texas logs bucket"
}

# ############################
# # Performance
# ############################

variable "service_prefix" {
  description = "Name for the Service prefix"
}

variable "project_group_short" {
  description = "Short name for the project group"
}

variable "programme" {
  description = "Shorthand name of the project programme"
}

variable "k8s_app_namespace" {
  description = "Name of the kubernetes namespace"
}
