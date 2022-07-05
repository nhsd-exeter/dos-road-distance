import boto3
import json
import os
import bcrypt
import time
from authlogger import AuthLogger

client = boto3.client("secretsmanager")
logger: AuthLogger = AuthLogger()


def authorize_api_request(event, context) -> dict:
    print("Event: {}".format(event))
    logger.log("Event: {}".format(event))
    noauth = True if "x-noauth" in event["headers"].keys() else False
    if noauth:
        logger.log("Noauth requested")
    try:
        if check_authorisation_token(event["headers"]["x-authorization"], noauth):
            response = {"isAuthorized": True}
    except Exception as e:
        print("Authentication method failed with error: {}".format(e))
        response = {
            "isAuthorized": False,
            "cloudWatchStreamName:": context.context.log_stream_name or '',
            "cloudWatchLogGroupName:": context.context.log_group_name or '',
            "lambdaFunctionArn:": context.invoked_function_arn or '',
            "lambdaRequestId:": context.context.aws_request_id or '',
            "lambdaMemoryLimit:": context.context.memory_limit_in_mb or ''
        }
    print("Response: {}".format(response))
    return response


def check_authorisation_token(token_hash_sent: str, noauth: bool) -> bool:
    if noauth and os.environ.get("DRD_ALLOW_NO_AUTH", False):
        logger.log("Noauth actioned as allowed")
        return True
    secrets_response = client.get_secret_value(
        SecretId=os.environ["SECRET_STORE"],
    )
    secrets = json.loads(secrets_response["SecretString"])
    time_factor = str(int(time.time() / 1800))
    token = str(secrets["ROAD_DISTANCE_API_TOKEN"]) + time_factor
    return bcrypt.checkpw(token.encode("utf-8"), token_hash_sent.encode("utf-8"))
