# Unit tests for authoriser lambda

test_handler.py  - tests covering core methods for authorisation

## Running the tests

Run the following commands from within the top level directory

### Individual tests
    make run-authoriser-test

### All tests

    make run-unit-test

### Selective tests
If you just want to run an individual test, you can specify it by name - e.g.

    make run-authoriser-test NAME=test_content_provider_response_success_per_destination

### The logs for the tests

The logs are located in `tests/unit/logs/auth.log` which gets cleared down before each test run.
If you want to analyse the log output then run a single test and review this file.
