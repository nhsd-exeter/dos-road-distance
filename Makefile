PROJECT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(abspath $(PROJECT_DIR)/build/automation/init.mk)

# ==============================================================================
# Development workflow targets

setup: # Set up project
	make project-config
	make python-virtualenv PYTHON_VENV_NAME=$(PROJECT_ID)
	pip install -r $(APPLICATION_DIR)/roaddistance/requirements.txt

build: # Build image
	make docker-build-lambda AWS_ECR=$(AWS_LAMBDA_ECR)
	make docker-build-auth AWS_ECR=$(AWS_LAMBDA_ECR)

start: project-start

restart:
	make \
		stop \
		start

stop: project-stop

log:
	docker logs --tail 50 --follow roaddistance-lambda

bash:
	docker exec --interactive --tty roaddistance-lambda bash

unit-test: # Test project
	if [ $(PROFILE) == local ]; then
		make local-unit-test
	else
		make start
		make run-unit-test
		make stop
	fi

push: # Push project artefacts to the registry
	eval "$$(make aws-assume-role-export-variables)"
	make docker-push NAME=roaddistance-lambda AWS_ECR=$(AWS_LAMBDA_ECR)
	make docker-push NAME=authoriser-lambda AWS_ECR=$(AWS_LAMBDA_ECR)

deploy: # Deploy artefacts - mandatory: PROFILE=[name]
	make sls-deploy STACK=application PROFILE=$(PROFILE)

provision: # Provision environment - mandatory: PROFILE=[name],STACKS=[comma separated names]
	eval "$$(make secret-fetch-and-export-variables)"
	make terraform-apply-auto-approve PROFILE=$(PROFILE) STACKS=$(STACKS)

clean:
	make stop
	docker network rm $(DOCKER_NETWORK) 2> /dev/null ||:

# ==============================================================================
# Supporting targets

trust-certificate: ssl-trust-certificate-project ## Trust the SSL development certificate

# --------------------------------------

build-tester: # Builds image used for testing - mandatory: PROFILE=[name]
	make docker-image NAME=tester

push-tester: # Pushes image used for testing - mandatory: PROFILE=[name]
	make docker-push NAME=tester

coverage:
	echo "Sending image $$(make _docker-get-reg)/tester:latest"
	make docker-run-tools IMAGE=$$(make _docker-get-reg)/tester:latest SH=y DIR=$(or $(DIR), $(APPLICATION_DIR_REL)) ARGS="$(ARGS)" CMD=" \
		cd /project/application/roaddistance/ && \
		python -m coverage run \
			--omit=tests/*,utilities/* \
			-m pytest && \
			python -m coverage xml"


upgrade-pip:
	make docker-run-tools \
		CMD="/usr/local/bin/python -m pip install --upgrade pip" \
		DIR=$(APPLICATION_DIR_REL)/roaddistance

python-requirements:
	make docker-run-tools \
		CMD="pip install -r requirements.txt" \
		DIR=$(APPLICATION_DIR_REL)/roaddistance

local-unit-test: # Run unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests, TEST_FILE=filename to specify a test file to pickup
	if [ -z $(TEST_FILE) ]; then
		echo "Running local unit test without test file"
		CMD="pip install -r requirements.txt; python -m pytest"
	else
		echo "Running local unit test with test file $(TEST_FILE)"
		CMD="pip install -r requirements.txt; python -m pytest -rA -q tests/unit/$(TEST_FILE) -k '$(NAME)'"
	fi
	make docker-run-tools SH=y DIR=$(or $(DIR), $(APPLICATION_DIR_REL)/roaddistance) \
		ARGS="--env PYTHONPATH=/tmp/.packages:$(APPLICATION_DIR_REL)/roaddistance" \
		CMD="$$CMD"

local-auth-unit-test: # Run autoriser unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ -z $(TEST_FILE) ]; then
		echo "Running local unit test without test file"
		CMD="pip install -r requirements.txt; python -m pytest"
	else
		echo "Running local unit test with test file $(TEST_FILE)"
		CMD="pip install -r requirements.txt; python -m pytest -rA -q tests/unit/$(TEST_FILE) -k '$(NAME)'"
	fi
	make docker-run-tools SH=y DIR=$(or $(DIR), $(APPLICATION_DIR_REL)/authoriser) \
		ARGS="--env PYTHONPATH=/tmp/.packages:$(APPLICATION_DIR_REL)/authoriser" \
		CMD="$$CMD"

run-unit-test: # Run unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(BUILD_ID) == 0 ]; then
		CONTAINER=roaddistance-lambda
	else
		CONTAINER=roaddistance-lambda-$(BUILD_ID)
	fi
	echo "Using container $$CONTAINER"
	if [ -z $(TEST_FILE) ]; then
			echo "Running $$CONTAINER unit test without test file"
			docker exec $$CONTAINER \
			/bin/sh -c 'for f in tests/unit/test_*.py; do echo "$$f:"; python -m pytest -rsx -q $$f; done'
	else
		echo "Running $$CONTAINER unit test with test file $(TEST_FILE)"
		docker exec $$CONTAINER \
		python -m pytest -rA -q tests/unit/$(TEST_FILE) -k "$(NAME)"
	fi

run-auth-unit-test: # Run authoriser tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(BUILD_ID) == 0 ]; then
		CONTAINER=authoriser-lambda
	else
		CONTAINER=authoriser-lambda-$(BUILD_ID)
	fi
	if [ -z $(TEST_FILE) ]; then
			echo "Running $$CONTAINER unit test without test file"
			docker exec $$CONTAINER \
			/bin/sh -c 'for f in tests/unit/test_*.py; do echo "$$f:"; python -m pytest -rsx -q $$f; done'
	else
			echo "Running $$CONTAINER unit test with test file $(TEST_FILE)"
			docker exec $$CONTAINER \
			python -m pytest -rA -q tests/unit/$(TEST_FILE) -k "$(NAME)"
	fi

run-contract-test: # Run contract only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(PROFILE) == local ]; then
		make local-unit-test TEST_FILE=test_contracts.py
	else
		make run-unit-test TEST_FILE=test_contracts.py
	fi

run-logging-test: # Run logging only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(PROFILE) == local ]; then
		make local-unit-test TEST_FILE=test_logging.py
	else
		make run-unit-test TEST_FILE=test_logging.py
	fi

run-handler-test: # Run handler only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(PROFILE) == local ]; then
		make local-unit-test TEST_FILE=test_handler.py
	else
		make run-unit-test TEST_FILE=test_handler.py
	fi

run-roaddistance-test: # Run road distance only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(PROFILE) == local ]; then
		make local-unit-test TEST_FILE=test_roaddistance.py
	else
		make run-unit-test TEST_FILE=test_roaddistance.py
	fi

run-traveltimerequest-test: # Run TravelTime protobuf request only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(PROFILE) == local ]; then
		make local-unit-test TEST_FILE=test_traveltimerequest.py
	else
		make run-unit-test TEST_FILE=test_traveltimerequest.py
	fi

run-traveltimeresponse-test: # Run TravelTime protobuf response only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(PROFILE) == local ]; then
		make local-unit-test TEST_FILE=test_traveltimeresponse.py
	else
		make run-unit-test TEST_FILE=test_traveltimeresponse.py
	fi

run-mock-test: # Run mock TravelTime protobuf only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(PROFILE) == local ]; then
		make local-unit-test TEST_FILE=test_mock.py
	else
		make run-unit-test TEST_FILE=test_mock.py
	fi

run-authoriser-test:
	if [ $(PROFILE) == local ]; then
		make local-auth-unit-test TEST_FILE=test_handler.py
	else
		make run-auth-unit-test TEST_FILE=test_handler.py
	fi

generate-contract-json: # Generate the JSON files used for contract testing
	cd $(APPLICATION_DIR)/roaddistance && \
		python yaml_to_json.py

generate-proto-python: # Generate the Python code from the protobuf proto files
	SRC_DIR=$(APPLICATION_DIR)/roaddistance/proto/traveltime && \
	DST_DIR=$(APPLICATION_DIR)/roaddistance/proto/traveltime&& \
	protoc -I=$$SRC_DIR --python_out=$$DST_DIR $$SRC_DIR/*.proto && \
	ls -l $$SRC_DIR/*.py

docker-build-lambda: # Build the local lambda Docker image
	rm -rf $(DOCKER_DIR)/roaddistance-lambda/assets/*
	mkdir $(DOCKER_DIR)/roaddistance-lambda/assets/log
	cp $(DOCKER_DIR)/roaddistance-lambda/.bashrc $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp $(APPLICATION_DIR)/roaddistance/requirements.txt $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp $(APPLICATION_DIR)/roaddistance/*.py $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp -r $(APPLICATION_DIR)/roaddistance/proto $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp -r $(APPLICATION_DIR)/roaddistance/openapi_schemas $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp -r $(APPLICATION_DIR)/roaddistance/mock $(DOCKER_DIR)/roaddistance-lambda/assets/
	make docker-image NAME=roaddistance-lambda
	rm -rf $(DOCKER_DIR)/roaddistance-lambda/assets/*

docker-build-auth: # Build the local lambda Docker image
	rm -rf $(DOCKER_DIR)/authoriser-lambda/assets/*
	cp $(APPLICATION_DIR)/authoriser/*.py $(DOCKER_DIR)/authoriser-lambda/assets/
	cp $(APPLICATION_DIR)/authoriser/requirements.txt $(DOCKER_DIR)/authoriser-lambda/assets/
	make docker-image NAME=authoriser-lambda
	rm -rf $(DOCKER_DIR)/authoriser-lambda/assets/*

docker-update-root: # Update the root files on the running lambda docker container without a rebuild
		docker exec \
			roaddistance-lambda \
			cp -v application/roaddistance/*.py ./

local-ccs-lambda-request: # Perform a sample valid request from CCS to the local lambda instance, which must be already running using make docker-run-lambda
	curl -v -POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
		-d @application/roaddistance/tests/unit/test_json/dos_road_distance_api_happy.json

local-ccs-lambda-request-invalid: # Perform a sample valid request from CCS to the local lambda instance, which must be already running using make docker-run-lambda
	curl -v -POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
		-d @application/roaddistance/tests/unit/test_json/dos_road_distance_api_invalid_missing_element.json

# --------------------------------------

lambda-alias: ### Updates new lambda version with alias based on commit hash - Mandatory PROFILE=[profile]
	eval "$$(make aws-assume-role-export-variables)"
	function=$(SERVICE_PREFIX)-rd-lambda
	versions=$$(make -s aws-lambda-get-latest-version NAME=$$function)
	version=$$(echo $$versions | make -s docker-run-tools CMD="jq '.Versions[-1].Version'" | tr -d '"')
	make aws-lambda-create-alias NAME=$$function VERSION=$$version

aws-lambda-get-latest-version: ### Fetches the latest function version for a lambda function - Mandatory NAME=[lambda function name]
	make -s docker-run-tools ARGS="$$(echo $(AWSCLI) | grep awslocal > /dev/null 2>&1 && echo '--env LOCALSTACK_HOST=$(LOCALSTACK_HOST)' ||:)" CMD=" \
		$(AWSCLI) lambda list-versions-by-function \
			--function-name $(NAME) \
			--output json \
		"

aws-lambda-create-alias: ### Creates an alias for a lambda version - Mandatory NAME=[lambda function name], VERSION=[lambda version]
	ALIAS_SUFFIX=""
	if [ "$(TF_VAR_drd_mock)" == "True" ]; then
		ALIAS_SUFFIX="-mock"
	fi
	make -s docker-run-tools ARGS="$$(echo $(AWSCLI) | grep awslocal > /dev/null 2>&1 && echo '--env LOCALSTACK_HOST=$(LOCALSTACK_HOST)' ||:)" CMD=" \
		$(AWSCLI) lambda create-alias \
			--name $(VERSION)-$(BUILD_COMMIT_HASH)$$ALIAS_SUFFIX \
			--function-name $(NAME) \
			--function-version $(VERSION) \
		"

# --------------------------------------

deployment-summary: # Returns a deployment summary
	echo Terraform Changes
	cat /tmp/terraform_changes.txt | grep -E 'Apply...'

pipeline-send-notification: ## Send Slack notification with the pipeline status - mandatory: PIPELINE_NAME,BUILD_STATUS
	eval "$$(make aws-assume-role-export-variables)"
	eval "$$(make secret-fetch-and-export-variables NAME=$(DEPLOYMENT_SECRETS))"
	make slack-it

propagate: # Propagate the image to production ecr - mandatory: BUILD_COMMIT_HASH=[image hash],GIT_TAG=[git tag],ARTEFACTS=[comma separated list]
	eval "$$(make aws-assume-role-export-variables PROFILE=$(PROFILE))"
	for image in $$(echo $(or $(ARTEFACTS), $(ARTEFACT)) | tr "," "\n"); do
		make docker-image-find-and-version-as COMMIT=$(BUILD_COMMIT_HASH) NAME=$$image TAG=$(GIT_TAG) AWS_ECR=$(AWS_LAMBDA_ECR)
	done

parse-profile-from-tag: # Return profile based off of git tag - Mandatory GIT_TAG=[git tag]
	echo $(GIT_TAG) | cut -d "-" -f2

tag: # Tag commit for production deployment as `[YYYYmmddHHMMSS]-[env]` - mandatory: PROFILE=[profile name],COMMIT=[hash]
	hash=$$(make git-hash COMMIT=$(COMMIT))
	make git-tag-create-environment-deployment PROFILE=$(PROFILE) COMMIT=$$hash

# --------------------------------------

performance-build: # mandatory - PROFILE=[name]
	rm -rf $(DOCKER_DIR)/performance/assets/locust/*
	cp $(APPLICATION_TEST_DIR)/performance/*.py $(DOCKER_DIR)/performance/assets/locust/
	cp $(APPLICATION_TEST_DIR)/performance/requirements.txt $(DOCKER_DIR)/performance/assets/locust/
	cp $(APPLICATION_TEST_DIR)/performance/locust.conf $(DOCKER_DIR)/performance/assets/locust/
	cp -r $(APPLICATION_DIR)/roaddistance/mock $(DOCKER_DIR)/performance/assets/locust/mock/
	make docker-image NAME=performance AWS_ECR=$(AWS_LAMBDA_ECR)
	rm -rf $(DOCKER_DIR)/performance/assets/locust/*

performance-push: # Push performance image to ECR
	eval "$$(make aws-assume-role-export-variables PROFILE=nonprod)"
	make docker-push NAME=performance AWS_ECR=$(AWS_LAMBDA_ECR)

performance-deploy: # mandatory - SECONDS=[time of performance]
	eval "$$(make aws-assume-role-export-variables PROFILE=nonprod)"
	eval "$$(make secret-fetch-and-export-variables ENVIRONMENT=nonprod)"
	make k8s-deploy STACK=performance PROFILE=nonprod AWS_ECR=$(AWS_LAMBDA_ECR)
	make k8s-job-tester-wait-to-complete TESTER_NAME=$(SERVICE_PREFIX)-performance SECONDS=$(SECONDS) AWS_ECR=$(AWS_LAMBDA_ECR) PROFILE=nonprod

performance-delete: # Delete performance deployment
	eval "$$(make aws-assume-role-export-variables PROFILE=nonprod)"
	make k8s-undeploy PROFILE=nonprod AWS_ECR=$(AWS_LAMBDA_ECR)
	make aws-ecr-untag NAME=performance TAG=$$(make docker-image-get-version NAME=performance) INCLUDE_LATEST=true

performance-start: # Start performance testing locally
	if [ nonprod != local ]; then
		eval "$$(make secret-fetch-and-export-variables ENVIRONMENT=nonprod)"
	fi
	make docker-image-start NAME=performance AWS_ECR=$(AWS_LAMBDA_ECR)

performance-stop:
	make docker-image-stop NAME=performance AWS_ECR=$(AWS_LAMBDA_ECR)

performance-test: # mandatory - PROFILE=[name]
	make performance-stop
	make performance-build
	make performance-start

performance-clean:
	rm -rf $(APPLICATION_TEST_DIR)/performance/results/*

performance-download:
	eval "$$(make aws-assume-role-export-variables)"
	make aws-s3-download FILE=$(FILE) URI=$(SERVICE_PREFIX)-performance

# ==============================================================================

create-artefact-repositories: # Create ECR repositories to store the artefacts
	make docker-create-repository NAME=roaddistance-lambda AWS_ECR=$(AWS_LAMBDA_ECR)
	make docker-create-repository NAME=authoriser-lambda AWS_ECR=$(AWS_LAMBDA_ECR)
	make docker-create-repository NAME=performance AWS_ECR=$(AWS_LAMBDA_ECR)

# ==============================================================================
.SILENT: \
	local-unit-test \
	local-auth-unit-test \
	parse-profile-from-tag \
	run-contract-test \
	run-unit-test \
	run-auth-unit-test
