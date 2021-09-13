-include $(VAR_DIR)/profile/dev.mk

# ==============================================================================
# Service variables

PROJECT_IMAGE_TAG :=
ENV := task
SERVICE_PREFIX := $(PROJECT_ID)-$(ENVIRONMENT)

# ==============================================================================
# Infrastructure variables

STACKS := lambda,api-gateway
