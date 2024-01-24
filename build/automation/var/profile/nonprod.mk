-include $(VAR_DIR)/platform-texas/v1/account-live-k8s-nonprod.mk

# ==============================================================================
# Service variables

PROJECT_IMAGE_TAG :=
ENV := nonprod
SERVICE_PREFIX := $(PROJECT_ID)-$(ENV)
AWS_LAMBDA_ECR = $(or $(AWS_ACCOUNT_ID), 000000000000).dkr.ecr.$(AWS_DEFAULT_REGION).amazonaws.com

# ==============================================================================
# Infrastructure variables

STACKS := secrets,lambda,api-gateway

TF_VAR_image_version := $(or $(BUILD_TAG), latest)
TF_VAR_deployment_secrets := $(DEPLOYMENT_SECRETS)
TF_VAR_drd_allow_no_auth := True
TF_VAR_lambda_tf_state_key := $(PROJECT_ID)/$(ENV)/lambda/terraform.state
TF_VAR_api_gateway_tf_state_key := $(PROJECT_ID)/$(ENV)/api-gateway/terraform.state
TF_VAR_s3_tf_state_key := $(PROJECT_ID)/$(ENV)/s3/terraform.state
TF_VAR_codebuild_tf_state_key := $(PROJECT_ID)/$(ENV)/codebuild/terraform.state
