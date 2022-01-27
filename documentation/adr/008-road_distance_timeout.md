# ADR-008: Road Distance Timeout

* Date: 2022/01/21
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Tamara Goldschmidt, Declan Heard, Christian Martin

## Context

Road Distance Phase 1 will implement a time to live (TTL) timeout on the lambda to prevent the road distance search taking longer than necessary, based upon previous performance runs. Though this is already an essential requirement, it is also being implemented as an initial step before the failover system is implemented later - therefore preventing excessive search times causing alerts to first line support which would trigger when the average response times breach 3.2 seconds. Currently our average response times are at around 1.1 seconds.

## Decision

The previous performance runs showed maximum times of around 1.7 seconds to traveltime under extreme load scenarios. We have, therefore, taken the decision to initially set the TTL to 2000 milliseconds for the lambda to ensure delayed requests will start to failover to crows-flies search.

## Consequences

The users will have longer search times during a degredation of road distance service but remaining broadly within the maximum average query times. This would only affect those users with the road distance permission, and therefore a manual mechanism exists to remove this component during a significant event. If the external provider (TravelTime) was down this failure response would be rapid, therefore this is limited to a scenario of degraded performance.
