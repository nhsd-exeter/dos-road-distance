ORG_NAME = nhsd-exeter
PROGRAMME = uec
PROJECT_GROUP = uec/tools
PROJECT_GROUP_SHORT = uec-tools
PROJECT_NAME = make-devops
PROJECT_NAME_SHORT = mdo
PROJECT_DISPLAY_NAME = Make DevOps
PROJECT_ID = $(PROJECT_GROUP_SHORT)-$(PROJECT_NAME_SHORT)

ROLE_PREFIX = UECCommon
PROJECT_TAG = $(PROJECT_NAME)
SERVICE_TAG = $(PROJECT_GROUP_SHORT)
SERVICE_TAG_COMMON = texas

PROJECT_TECH_STACK_LIST = python

DOCKER_REPOSITORIES =
SSL_DOMAINS_PROD =
DEPLOYMENT_SECRETS = $(PROJECT_ID)-$(PROFILE)/deployment
