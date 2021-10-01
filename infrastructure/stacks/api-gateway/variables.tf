##########################
# INFRASTRUCTURE COMPONENT
##########################

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
# # UEC COMMON
# ##############

variable "profile" {
  description = "The tag used to identify profile e.g. dev, test, live, ..."
}

variable "programme" {
  description = "The programme in which the service belongs to"
}

variable "service_prefix" {
  description = "The service prefix for the application"
}

variable "texas_terraform_state_store" {
  description = "State store for terraform"
}

variable "environment" {
  description = "Environment of the infrastructure"
}

# ##############
# # API GATEWAY
# ##############

variable "lambda_tf_state_key" {
  description = "State store for lambda stack terraform"
}
