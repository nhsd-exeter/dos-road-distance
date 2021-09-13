-include $(VAR_DIR)/platform-texas/v1/account-live-k8s-nonprod.mk

# ==============================================================================
# Service variables

PROJECT_IMAGE_TAG :=
ENV := dev
SERVICE_PREFIX := $(PROJECT_ID)-$(ENV)

# ==============================================================================
# Infrastructure variables

STACKS := secrets,lambda,api-gateway

TF_VAR_lambda_tf_state_key := $(PROJECT_ID)/$(ENVIRONMENT)/lambda/terraform.state
