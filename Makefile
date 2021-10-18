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

log: project-log

bash:
	docker exec --interactive --tty roaddistance-lambda bash

unit-test: # Test project
	make start
	make run-unit-test
	make stop

push: # Push project artefacts to the registry
	eval "$$(make aws-assume-role-export-variables)"
	make docker-push NAME=roaddistance-lambda AWS_ECR=$(AWS_LAMBDA_ECR)
	make docker-push NAME=authoriser-lambda AWS_ECR=$(AWS_LAMBDA_ECR)

deploy: # Deploy artefacts - mandatory: PROFILE=[name]
	make sls-deploy STACK=application PROFILE=$(PROFILE)

provision: # Provision environment - mandatory: PROFILE=[name],STACKS=[comma separated names]
	eval "$$(make secret-fetch-and-export-variables)"
	make terraform-apply-auto-approve PROFILE=$(PROFILE) STACKS=$(STACKS)

# ==============================================================================
# Supporting targets

trust-certificate: ssl-trust-certificate-project ## Trust the SSL development certificate

# --------------------------------------

run-unit-test: # Run unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	if [ $(BUILD_ID) == 0 ]; then
		container=roaddistance-lambda
	else
		container=roaddistance-lambda-$(BUILD_ID)
	fi
	if [ -z $(TEST_FILE) ]; then
			docker exec $$container \
			/bin/sh -c 'for f in tests/unit/test_*.py; do python -m pytest -rsx -q $$f; done'
	else
			docker exec $$container \
			python -m pytest -rA -q tests/unit/$(TEST_FILE) -k "$(NAME)"
	fi

run-contract-test: # Run contract only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_contracts.py

run-logging-test: # Run logging only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_logging.py

run-handler-test: # Run handler only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_handler.py

run-roaddistance-test: # Run road distance only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_roaddistance.py

run-traveltimerequest-test: # Run TravelTime protobuf request only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_traveltimerequest.py

run-traveltimeresponse-test: # Run TravelTime protobuf response only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_traveltimeresponse.py

run-mock-test: # Run mock TravelTime protobuf only unit tests, add NAME="xxx" or NAME="xxx or yyy" to run specific tests
	make run-unit-test TEST_FILE=test_mock.py

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
	cp $(APPLICATION_DIR)/roaddistance/requirements.txt $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp $(APPLICATION_DIR)/roaddistance/*.py $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp -r $(APPLICATION_DIR)/roaddistance/proto $(DOCKER_DIR)/roaddistance-lambda/assets/
	cp -r $(APPLICATION_DIR)/roaddistance/openapi_schemas $(DOCKER_DIR)/roaddistance-lambda/assets/
	if [ $(TF_VAR_drd_mock) != "False" ]; then
		cp -r $(APPLICATION_DIR)/roaddistance/mock $(DOCKER_DIR)/roaddistance-lambda/assets/
	fi
	make docker-image NAME=roaddistance-lambda
	rm -rf $(DOCKER_DIR)/roaddistance-lambda/assets/*

docker-build-auth: # Build the local lambda Docker image
	rm -rf $(DOCKER_DIR)/authoriser-lambda/assets/*
	cp $(APPLICATION_DIR)/authoriser/*.py $(DOCKER_DIR)/authoriser-lambda/assets/
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
		-d @application/roaddistance/tests/unit/test_json/dos_road_distance_api_invalid_coord.json

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
	make -s docker-run-tools ARGS="$$(echo $(AWSCLI) | grep awslocal > /dev/null 2>&1 && echo '--env LOCALSTACK_HOST=$(LOCALSTACK_HOST)' ||:)" CMD=" \
		$(AWSCLI) lambda create-alias \
			--name $(VERSION)-$(BUILD_COMMIT_HASH) \
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

propagate: # Propagate the image to production ecr - mandatory: BUILD_COMMIT_HASH=[image hash],GIT_TAG=[git tag]
	make artefact-pull-and-retag COMMIT=$(BUILD_COMMIT_HASH) ARTEFACTS=roaddistance-lambda,authoriser-lambda TAG=$(GIT_TAG) PROFILE=nonprod
	make artefact-propagate TAG=$(GIT_TAG) ARTEFACTS=roaddistance-lambda,authoriser-lambda PROFILE=$(PROFILE)

artefact-pull-and-retag: # Pulls image from nonprod and retags it ready for production - mandatory: COMMIT=[commit hash]TAG=[image tag],ARTEFACTS=[comma separated list of images],PROFILE=[profile]
	eval "$$(make aws-assume-role-export-variables PROFILE=$(PROFILE))"
	for image in $$(echo $(or $(ARTEFACTS), $(ARTEFACT)) | tr "," "\n"); do
		hash=$$(make git-hash COMMIT=$(COMMIT))
		digest=$$(make docker-image-get-digest NAME=$$image TAG=$$hash)
		make docker-pull NAME=$$image DIGEST=$$digest AWS_ECR=$(AWS_LAMBDA_ECR)
		docker tag $(AWS_LAMBDA_ECR)/$(PROJECT_GROUP_SHORT)/$(PROJECT_NAME_SHORT)/$$image@$$digest \
			$(AWS_ACCOUNT_ID_PROD).dkr.ecr.$(AWS_DEFAULT_REGION).amazonaws.com/$(PROJECT_GROUP_SHORT)/$(PROJECT_NAME_SHORT)/$$image:$(TAG)
	done

artefact-propagate: # Pushes image to production - mandatory:TAG=[image tag],ARTEFACTS=[comma separated list of images],PROFILE=[profile]
	eval "$$(make aws-assume-role-export-variables PROFILE=$(PROFILE))"
	for image in $$(echo $(or $(ARTEFACTS), $(ARTEFACT)) | tr "," "\n"); do
		make docker-push NAME=$$image TAG=$(TAG) AWS_ECR=$(AWS_LAMBDA_ECR)
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

performance-push: # mandatory - PROFILE=[name]
	eval "$$(make aws-assume-role-export-variables)"
	make docker-push NAME=performance AWS_ECR=$(AWS_LAMBDA_ECR)

performance-deploy: # mandatory - PROFILE=[name], SECONDS=[time of performance]
	eval "$$(make aws-assume-role-export-variables)"
	eval "$$(make secret-fetch-and-export-variables ENVIRONMENT=nonprod)"
	make k8s-deploy STACK=performance AWS_ECR=$(AWS_LAMBDA_ECR)
	make k8s-job-tester-wait-to-complete TESTER_NAME=$(SERVICE_PREFIX)-performance SECONDS=$(SECONDS) AWS_ECR=$(AWS_LAMBDA_ECR)

performance-delete: # mandatory - PROFILE=[name]
	eval "$$(make aws-assume-role-export-variables)"
	make k8s-undeploy AWS_ECR=$(AWS_LAMBDA_ECR)

performance-start: # mandatory - PROFILE=[name]
	if [ $(PROFILE) != local ]; then
		eval "$$(make secret-fetch-and-export-variables)"
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
	parse-profile-from-tag
