# ADR-006: Road Distance - Wrapper for 3rd-party API

* Date: 2021/03/22
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Tamara Goldschmidt, Declan Heard

## Context

The DoS service requires a mechanism for sending requests and receiving responses from the 3rd-party road distance API.

## Decision

The API wrapper will be implemented as a microservice, deployed as an AWS Lambda. This will consist of:

* A separate component that can be re-used within the Core DoS service or the DoS product family
* A minimal API interface to meet the business need of finding the distance from a single origin to multiple destinations
* A distance supplier agnostic API allowing less tie-in to the external service

## Consequences

The development of a microservice requires additional development time and an initial learning curve within the team to run it on unfamiliar infrastructure.

Separating this code from the core DoS application enables easier maintenance, automatic scaling, and makes the functionality accessible to other applications.

Uncoupled from DoS the coding language is not limited to PHP, and technology can be selected that matches the longer term business aspirations.
