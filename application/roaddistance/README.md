# AWS Lambda Docker

## Requirements

    pip install awslambdaric

## Container image settings

Lambda supports the following container image settings in the Dockerfile:

* ENTRYPOINT – Specifies the absolute path to the entry point of the application.
* CMD – Specifies parameters that you want to pass in with ENTRYPOINT.
* WORKDIR – Specifies the absolute path to the working directory.
* ENV – Specifies an environment variable for the Lambda function.

## Container image environment variables

The AWS base images provide the following environment variables:
```
LAMBDA_TASK_ROOT=/var/task
LAMBDA_RUNTIME_DIR=/var/runtime
```
## Building and running

    make docker-build-lambda
    make docker-run-lambda

Then, in another shell instance, a sample request can be made:

    make local-ccs-lambda-request


# RDLogger.py usage notes
## Usage
```
from rdlogger import RDLogger
rdlogger = RDLogger()
rdlogger.log("Put your info log message here")
rdlogger.log_formatted(request, "ccs_request")
rdlogger.log_ccs_error("422", "there was an error", <data> = "")
rdlogger.log_formatted(request, "provider_request")
rdlogger.log_formatted(request, "provider_response")
rdlogger.log_provider_success("1000001", "no", 1000)
rdlogger.log_provider_success("1000001", "yes")
rdlogger.log_provider_error("422", "there was an error", <data> = "")
```
## Log format outputs
### Basic Log
```
YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|road_distance|<message>
YYYY/MM/DD 00:00:00.000000+0100|error|lambda|<request_id>|<transaction_id>|road_distance|<message>
```
### Status Log - basic status/info (e.g. summary of provider response)
```
YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|road_distance|system|success|message=<message>
```

### Raw request and response
```
YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|road_distance|ccsrequest|<data>
YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|road_distance|providerrequest|<data>
YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|road_distance|providerresponse|<data>
```

### CCS Request Failure
```
YYYY/MM/DD 00:00:00.000000+0100|error|lambda|<request_id>|<transaction_id>|road_distance|ccsrequest|failed|statuscode=<statuscode>|error=<error>|data=<data>
```

### Provider Response Failure (anything other than 200 response)
```
YYYY/MM/DD 00:00:00.000000+0100|error|lambda|<request_id>|<transaction_id>|road_distance|providerresponse|failed|statuscode=<statuscode>|error=<error>|data=<data>
```

### Provider Response Success - Per returned service
```
YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|road_distance|providerresponse|success|reference=<serviceUid>|unreachable=<yes/no>|distance=####|km=##.#|miles=##.#
```
