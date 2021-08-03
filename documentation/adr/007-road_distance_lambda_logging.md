# ADR-007: Road Distance Lambda Logging

* Date: 2021/08/03
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Tamara Goldschmidt

## Context

The Road Distance pilot specifically sets out to log information on all the requests, responses and processing times for analysis. This document details all of the logging that will take place on the Lambda.

## Decision

The following information will be logged:
* Raw request received from CCS (Check Capacity Summary)
* Raw response from the provider
* Validation failures of request from CCS
* Validation failures of the response from the provider
* Error codes and descriptions in response from provider
* Each service ID and distance in the response from the provider (separately logged for each service)

The transaction ID is sent from CCS to link all of the requests and responses together. The application ID provides additional linking for when error states occur in the incoming request from CCS.

## Consequences

We must ensure details logs are maintained for all transactions and can be connected together with both the rquest and the services.
