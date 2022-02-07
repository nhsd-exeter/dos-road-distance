# ADR-002: API Authentication

* Date: 2022/02/07
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Tamara Goldschmidt, Declan Heard, Christian Martin, Livsey Williams, Sarah Harding

## Context
Our API needs to be kept private and accessible only to the authorised actors. For the application we only have one actor, the DoS CCS system. This document will additionally discuss other access protections.

## Options

* Lambda authorizers: This is the method we currently use, however as it is using Python code we can add more dynamicismn into this to make it more secure and robust
* JWT authorizers: This is for OpenID and Oauth connections - this would be useful if authenticating individuals, however our application is not doing this and therefore this would be vastly overkill and overcomplex.
* Standard AWS IAM roles and policies: The Lambda is not located in the same cluster to have access to the IAM roles, and therefore this would be not only a non-trivial solution but would also expose it unnecessarily therefore not best practice.


## Decision, Design and pseudocode

### Lambda authorizers
Our solution is a code level one remaining on the Lambda authorizers. The password, held in AWS secrets, will be bcrypt hashed with salt. This algorithm is strong and common for both PHP and Python.

### HTTPS requirement

It is a requirement that this communication is only permitted via HTTPS to ensure secure transmission preventing man in the middle. We may also need to ensure that the HTTPS certificate used is sending the details we expect as an additional check.

For the request we have ensured the salting cost be kept to a minimum as this is not a stored password, therefore we do not need the additional hardening required for a password database.

### PHP

```php
magic_string = '32bit string';
secrets_password = fetchPasswordFromS3().magic_string;
password_hash = password_hash(secrets_password, PASSWORD_BCRYPT, ['cost' => 4]);
```

### Python

```python
import bcrypt

magic_string = '32bit string';
secrets_password = fetchPasswordFromS3() + magic_string
password_hash = bcrypt.hashpw(secrets_password, bcrypt.gensalt())

// ------------ checking back

if bcrypt.checkpw(secrets_password, password_hash):
    print("match")
else:
    print("does not match")
```

## Consequences

* Relatively small update to the code to implement
* Does not require addition infrastructure
* Additional processing time cost will exist for the hashing and salting processing, we have kept this to a minimum
* The proposed solution hardens the security without exposing the Lambda to additional parts of the infrastructure such as IAM roles would
* Methods such as JWT would require additional calls to process, the proposed solution avoids this
