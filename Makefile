PROJECT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(abspath $(PROJECT_DIR)/build/automation/init.mk)

# ==============================================================================
# Development workflow targets

setup: # Set up project
	make project-config
	make python-virtualenv PYTHON_VENV_NAME=$(PROJECT_ID)
	pip install -r application/requirements.txt

build: project-config # Build project
	make docker-build NAME=NAME_TEMPLATE_TO_REPLACE

start: project-start # Start project

stop: project-stop # Stop project

restart: stop start # Restart project

log: project-log # Show project logs

test: # Test project
	make start
	make stop

push: # Push project artefacts to the registry
	make docker-push NAME=NAME_TEMPLATE_TO_REPLACE

deploy: # Deploy artefacts - mandatory: PROFILE=[name]
	make project-deploy STACK=application PROFILE=$(PROFILE)

provision: # Provision environment - mandatory: PROFILE=[name]
	make terraform-apply-auto-approve STACK=database PROFILE=$(PROFILE)

clean: # Clean up project

# ==============================================================================
# Supporting targets

trust-certificate: ssl-trust-certificate-project ## Trust the SSL development certificate

# ==============================================================================
# Pipeline targets

build-artefact:
	echo TODO: $(@)

publish-artefact:
	echo TODO: $(@)

backup-data:
	echo TODO: $(@)

provision-infractructure:
	echo TODO: $(@)

deploy-artefact:
	echo TODO: $(@)

apply-data-changes:
	echo TODO: $(@)

# --------------------------------------

run-static-analisys:
	echo TODO: $(@)

run-unit-test: # Run unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
		docker exec \
			roaddistance-lambda \
			python -m pytest -q tests/unit/$(TEST_FILE) -k "$(NAME)"

run-smoke-test:
	echo TODO: $(@)

run-integration-test:
	echo TODO: $(@)

run-contract-test: # Run contract only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_contracts.py

run-logging-test: # Run logging only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_logging.py

run-handler-test: # Run handler only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_handler.py

run-roaddistance-test: # Run road distance only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_roaddistance.py

run-traveltimerequest-test: # Run travel time protobuf request only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_traveltimerequest.py

run-traveltimeresponse-test: # Run travel time protobuf reponse only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_traveltimeresponse.py

run-functional-test:
	[ $$(make project-branch-func-test) != true ] && exit 0
	echo TODO: $(@)

run-performance-test:
	[ $$(make project-branch-perf-test) != true ] && exit 0
	echo TODO: $(@)

run-security-test:
	[ $$(make project-branch-sec-test) != true ] && exit 0
	echo TODO: $(@)

generate-contract-json: # Generate the JSON files used for contract testing
	cd application && \
		python yaml_to_json.py

generate-proto-python: # Generate the Python code from the protobuf proto files
	SRC_DIR=application/proto/traveltime && \
	DST_DIR=application/proto/traveltime&& \
	protoc -I=$$SRC_DIR --python_out=$$DST_DIR $$SRC_DIR/*.proto && \
	ls -l $$SRC_DIR/*.py

docker-build-lambda: # Build the local lambda Docker image
	cp $(APPLICATION_DIR)/requirements.txt $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp $(APPLICATION_DIR)/*.py $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp -r $(APPLICATION_DIR)/proto $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp -r $(APPLICATION_DIR)/openapi_schemas $(DOCKER_DIR)/roaddistance-lambda/assets/
	make docker-image NAME=roaddistance-lambda
	rm $(DOCKER_DIR)/roaddistance-lambda/assets/*.py

docker-run-lambda: # Run the local lambda Docker container
	docker run --rm -p 9000:8080 \
		--mount type=bind,source=$(APPLICATION_DIR)/tests,target=/var/task/tests \
		--mount type=bind,source=$(APPLICATION_DIR),target=/var/task/application \
		--name roaddistance-lambda $(DOCKER_REGISTRY)/roaddistance-lambda:latest
	# make docker-run IMAGE=$(DOCKER_REGISTRY)/roaddistance-lambda:latest \
	# 	ARGS="-p 9000:8080 --mount type=bind,source=$(APPLICATION_DIR)/tests,target=/var/task/tests" \
	# 	CONTAINER=roaddistance-lambda

docker-update-root: # Update the root files on the running lambda docker container without a rebuild
		docker exec \
			roaddistance-lambda \
			cp -v application/*.py ./

docker-bash-lambda: # Bash into the running lambda docker container
		docker exec -it \
			roaddistance-lambda \
			/bin/bash

local-ccs-lambda-request: # Perform a sample valid request from CCS to the local lambda instance, which must be already running using make docker-run-lambda
	curl -v -POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
		-d @application/tests/unit/test_json/dos_road_distance_api_happy.json

# --------------------------------------

remove-unused-environments:
	echo TODO: $(@)

remove-old-artefacts:
	echo TODO: $(@)

remove-old-backups:
	echo TODO: $(@)

# --------------------------------------

pipeline-finalise: ## Finalise pipeline execution - mandatory: PIPELINE_NAME,BUILD_STATUS
	# Check if BUILD_STATUS is SUCCESS or FAILURE
	make pipeline-send-notification

pipeline-send-notification: ## Send Slack notification with the pipeline status - mandatory: PIPELINE_NAME,BUILD_STATUS
	eval "$$(make aws-assume-role-export-variables)"
	eval "$$(make secret-fetch-and-export-variables NAME=$(PROJECT_GROUP_SHORT)-$(PROJECT_NAME_SHORT)-$(PROFILE)/deployment)"
	make slack-it

# --------------------------------------

pipeline-check-resources: ## Check all the pipeline deployment supporting resources - optional: PROFILE=[name]
	profiles="$$(make project-list-profiles)"
	# for each profile
	#export PROFILE=$$profile
	# TODO:
	# table: $(PROJECT_GROUP_SHORT)-$(PROJECT_NAME_SHORT)-deployment
	# secret: $(PROJECT_GROUP_SHORT)-$(PROJECT_NAME_SHORT)-$(PROFILE)/deployment
	# bucket: $(PROJECT_GROUP_SHORT)-$(PROJECT_NAME_SHORT)-$(PROFILE)-deployment
	# certificate: SSL_DOMAINS_PROD
	# repos: DOCKER_REPOSITORIES

pipeline-create-resources: ## Create all the pipeline deployment supporting resources - optional: PROFILE=[name]
	profiles="$$(make project-list-profiles)"
	# for each profile
	#export PROFILE=$$profile
	# TODO:
	# Per AWS accoount, i.e. `nonprod` and `prod`
	eval "$$(make aws-assume-role-export-variables)"
	#make aws-dynamodb-create NAME=$(PROJECT_GROUP_SHORT)-$(PROJECT_NAME_SHORT)-deployment ATTRIBUTE_DEFINITIONS= KEY_SCHEMA=
	#make secret-create NAME=$(PROJECT_GROUP_SHORT)-$(PROJECT_NAME_SHORT)-$(PROFILE)/deployment VARS=DB_PASSWORD,SMTP_PASSWORD,SLACK_WEBHOOK_URL
	#make aws-s3-create NAME=$(PROJECT_GROUP_SHORT)-$(PROJECT_NAME_SHORT)-$(PROFILE)-deployment
	#make ssl-request-certificate-prod SSL_DOMAINS_PROD
	# Centralised, i.e. `mgmt`
	eval "$$(make aws-assume-role-export-variables AWS_ACCOUNT_ID=$(AWS_ACCOUNT_ID_MGMT))"
	#make docker-create-repository NAME=NAME_TEMPLATE_TO_REPLACE
	#make aws-codeartifact-setup REPOSITORY_NAME=$(PROJECT_GROUP_SHORT)

# ==============================================================================

.SILENT:
