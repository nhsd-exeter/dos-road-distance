# Unit tests for road distance lambda

test_provider.py  - tests covering core methods for the handling of requests and calling external API

test_contracts.py - tests covering contract validation

## Running the tests

Run the following commands from within the top level directory

### Individual tests
    make run-contract-test
    make run-logging-test
    make run-handler-test
    make run-roaddistance-test
    make run-traveltimerequest-test
    make run-traveltimeresponse-test

### All tests

    make run-unit-test

### Selective tests
If you just want to run an individual test, you can specify it by name - e.g.

    make run-logging-test NAME=test_content_provider_response_success_per_destination

### The logs for the tests

The logs are located in `tests/unit/logs/rd.log` which gets cleared down before each test run. 
If you want to analyse the log output then run a single test and review this file
