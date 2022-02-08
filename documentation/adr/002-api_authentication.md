# ADR-002: API Authentication

* Date: 2022/02/07
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Declan Heard, Christian Martin, Livsey Williams, Sarah Harding

## Context
Our API needs to be kept private and accessible only to the authorised actors. For the application we only have one actor, the DoS CCS system. This document will additionally discuss other access protections.

## Options

### Authorizers

* Lambda authorizers: This is the method we currently use, however as it is using Python code we can add more dynamicismn into this to make it more secure and robust
* JWT authorizers: This is for OpenID and Oauth connections - this would be useful if authenticating individuals, however our application is not doing this and therefore this would be vastly overkill and overcomplex.
* Standard AWS IAM roles and policies: The Lambda is not located in the same cluster to have access to the IAM roles, and therefore this would not only be a non-trivial solution but would also expose it unnecessarily, therefore not best practice.

### Sessions or caching

Sessions or authorisation caching can also be used as a way to keep the connection alive for a limited period of time. This allows an already authenticated request to persist across multiple subsequent requests to prevent continuous hashing.

## Decision, Design and pseudocode

### Lambda authorizers

Our solution is a code level one remaining on the Lambda authorizers. The password, held in AWS secrets, will be bcrypt hashed with salt. This algorithm is strong and common for both PHP and Python.

For the request we have ensured the salting cost be kept to a minimum as this is not a stored password, therefore we do not need the additional hardening required for a password database.

We have also chosen to enable AWS authorisation token caching.
### HTTPS requirement

It is a requirement that this communication is only permitted via HTTPS to ensure secure transmission preventing man in the middle. We may also need to ensure that the HTTPS certificate used is sending the details we expect as an additional check.

### PHP

```php
$secrets_password = fetchPasswordFromSecrets() . time_factor;
$password_hash = password_hash($secrets_password, PASSWORD_BCRYPT, ['cost' => 4]));
```

### Python

```python
secrets_password = fetchPasswordFromS3() + time_factor
password_hash = bcrypt.hashpw(secrets_password, bcrypt.gensalt())

// ------------ checking back

if bcrypt.checkpw(secrets_password, password_hash):
    print("match")
else:
    print("does not match")
```

###  Token time chunking

We have added a time element onto the password string to ensure the token hash dies. This can be seen in the example code above. We chunk this interval into time blocks so that it can persist a token for a period of time before rejecting it.

### Client caching

We have used a time interval that is within the time period used for time chunking of the token password. The time interval used here segregates the regeneration periods required, therefore creating a caching period on the client by reusing the existing token. We may store this token using client sessions within PHP.

An example of how this could be implemented on the client:

```pseudocode
if previous_time < (time()/1800) {
  hashed_token = generate_token()
  previous_time = time()/1800
}
send_request(authorization = hashed_token)
```

### Authorisation caching

Authorisation caching will prevent the need for hashing of every request and therefore reduce the impact of the cost. The client would need to perform it's own TTL and token storage to resend if this is to be implemented.

> When caching is enabled for an authorizer, API Gateway uses the authorizer's identity sources as the cache key. If a client specifies the same parameters in identity sources within the configured TTL, API Gateway uses the cached authorizer result, rather than invoking your Lambda function.
> [Source](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html)

An example of how this could be implemented for the Lambda gateway:

* Enable Authorization Caching with TTL 1920
* New token received means new authorisation check and cache appended to

## Consequences

* Relatively small update to the code to implement
* Does not require addition infrastructure
* Additional processing time cost will exist for the hashing and salting processing, we have kept this to a minimum
* The proposed solution hardens the security without exposing the Lambda to additional parts of the infrastructure such as IAM roles would
* Methods such as JWT would require additional calls to process, the proposed solution avoids this
