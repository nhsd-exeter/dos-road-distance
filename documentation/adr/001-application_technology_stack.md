# ADR-001: Application Technology Stack

* Date: 2021/08/04
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Tamara Goldschmidt, Declan Heard

## Context
This will describe the technology stack being used throughout the system. It is intended to be a broad overview of intended technology but will be modified to include any new decision taken during the project.

## Decision

We have a container level diagram to give an outline of the system before delving into the technology used throughout:
![Road Distance Pilot Container Diagram](../diagrams/Road%20Distance%20Pilot%20-%202%20Containers.png)

### Core development
* Jenkins - the pipeline service
* Terraform - used to configure the infrastructure and components of the pipeline
* Code pipeline - AWS code pipeline for the Lambdas
* Serverless framework - to deploy and configure Lamdas
* AWS Lambdas - for the Road Distance service access
* Python - for the main development of the Road Distance application
* Cloudwatch - to capture the logs
* Firehose - used to push the Cloudwatch logs to Splunk
* Splunk - used to store and analyse the logs

### Testing
* Locust - load testing
* PyTest - unit testing

### Anciliary facilitators
* Github - to store the repository of code and documentation
* OpenAPI - provides the standard to define the contracts between the API endpoints (CCS to Lambda and Lambda to provider)

## Consequences

Choosing the correct components of the system is important for performance and interoperability.
