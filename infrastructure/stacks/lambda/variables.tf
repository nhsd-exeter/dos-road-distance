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

variable "project_group_short" {
  description = "Short name of the project group"
}

variable "project_name_short" {
  description = "Short name of the project"
}

# ##############
# # LAMBDA
# ##############

variable "image_version" {
  description = "The version of the Lambda docker image"
}
