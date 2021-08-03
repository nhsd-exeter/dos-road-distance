# ADR-003: Check Capacity Summary (CCS) Interface

* Date: 2021/08/03
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Tamara Goldschmidt

## Context
The Check Capacity Summary (CCS) service interfaces with the Road Distances API via an AWS Lambda. This document describes some of the decisions made for development of this interaction.

A requirement of the pilot is to ensure that there is a minimal impact on the CCS search service.

## Decision

Several design decision were taken in respect of CCS's interaction with the Road Distance API:
* The request will be made in JSON as this is inline with current requests being made throughout the system and easily handled in both PHP and Python
* We include a transaction ID so that the response can be tied back to the original CCS search
* We included "reference" in the request for each origin and destination to make it provider agnostic and to link results back to the services
* The request passes through a location ID rather than postcode for origins to mitigate issues storing PID
* The only responses returned to CCS will be status codes 200 and 500 with a blank body - this is to simplify the response and hide the internal workings in the case of errors from the provider
* Use of Guzzle asynchronous requests (fire and forget)

## Consequences

To ensure the search is not more than minimaly impacted the decisions taken were made to
* reduce the request and response sizes
* use of asynchronous requests ensures the CCS engine continues search processing without waiting for a response

The asynchronous request decisions taken for the pilot would not be possible in the final live version. In the pilot we log data on the road distances search for analysis, while minimising impact on the live system search response times. The final live version would need to receive the responses as part of the actual search.

While knowledge of the total request time during the pilot is essential, this will be done via logging of the additional time taken during the Lambda stage of the application - which links back using the transaction ID.
