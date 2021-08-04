# ADR-002: API Authentication

* Date: 2021/08/03
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Tamara Goldschmidt, Declan Heard

## Context
Our API needs to be kept private and accessible only to the authorised actors. For the purpose of the pilot version of Road Distance application we only have one actor, the DoS system. This document will additionally discuss other access protections.

## Decision

### Token authentication

A token authentication method will be used and held in AWS secrets. This will only allow access to the system by sending the correct API key.

It is a requirement that this communication is only permitted via HTTPS to ensure secure transmission preventing man in the middle. We may also need to ensure that the HTTPS certificate used is sending the details we expect as an additional check.

### IP restrictions

An additional protection of IP restriction will be put in place to further restrict access to this API.

## Consequences

### Tokens intended for pilot only

Token authentication is the method indended for the pilot stage of the application. However, we do not intend to distribute this token for additional onboarding. We should consider public/private keys as a potential future solution.

### IP restrictions

IP restrictions can be circumvented and on there own are not enough, however this is only being used here as an additional layer or protection.
