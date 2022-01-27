# ADR-005: Road Distance - Restricting User Access

* Date: 2021/03/22
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Declan Heard, Christian Martin

## Context

The move to road distances is a large change to a clinically critical search which would benefit from a staged rollout. There is also the possibility that some regions may not wish to have the search changed having already implemented other measures locally, such as Locally Defined Areas (LDAs).

## Decision

The solutions we have explored for allowing only specific users to access the new search functionality are:

* Creating a new version of the SOAP web service (1.6) which users could access separately
* Using a custom role provided to a subset of users providing access to the new functionality within the application

While versioning would be very quick to implement, the new search features are being developed on the basis that users calling the SOAP web service will not be required to make any changes to their internal systems. A separate check would also be needed if we wanted to prevent users access the new API version inadvertently.

Maintaining a list of users with access to the new search within the application requires additional maintenance, but ensures we retain control over access, and could be implemented via a role permission.

## Consequences

Additional code will be required to create the new role (permission) in the SOAP web service and Check Capacity Summary search chain in order to conditionally use the new functionality. However, these changes are trivial and, once implemented, user access can be managed via the UI without the need for further deployments. Requests for changes to user access may also be actioned immediately.
