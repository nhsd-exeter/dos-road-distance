# Response Contract Design

## Success structure

The response will have status 200, with a blank message, and include the transaction-id plus an array of destinations. The destinations will include the destination reference, unreachable status and the distance in metres.

## Fail structure

A failure status code will be 400 series if an error in contract or data based along with a message and the transaction-id. 500 series will be used for errors before the data is being processed - e.g. gateway issue, internal server error.

## Examples

### Success response

```json
{
 "status":200,
 "message":"",
 "transactionid":"43c31af7-1f53-470f-9edc-fed8f447dc8f",
 "destinations":[
  {
   "reference":"1001",
   "unreachable":"no",
   "distance":15595,
  },
  {
   "reference":"1001",
   "unreachable":"no",
   "distance":15595,
  }
 ]
}
```

### Fail responses

```json
{
 "status":400,
 "message":"Contract failed for response format",
 "transactionid":"43c31af7-1f53-470f-9edc-fed8f447dc8f"
}
```

```json
{
 "status":500,
 "message":"Contract failed for response format"
}
```
