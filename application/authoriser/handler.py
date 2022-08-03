import boto3
import json
import os
import bcrypt
import time
from authlogger import AuthLogger

logger: AuthLogger = AuthLogger()

def authorize_api_request(event, context) -> dict:
    response: dict = {"isAuthorized": False}
    print("Event: {}".format(event))
    logger.log("Event: {}".format(event))
    noauth = True if "x-noauth" in event["headers"].keys() else False
    if noauth:
        logger.log("Noauth requested")
        response = {"isAuthorized": True}
    try:
        if check_authorisation_token(event["headers"]["x-authorization"], noauth):
            response = {"isAuthorized": True}
    except Exception as e:
        print("Authentication method failed with error [{}]: {}, Arguments: {}".format(type(e).__name__, e, e.args))
    return response


def check_authorisation_token(token_hash_sent: str, noauth: bool) -> bool:
    client = boto3.client("secretsmanager")
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
