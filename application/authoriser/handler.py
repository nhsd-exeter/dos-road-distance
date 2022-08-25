import boto3
import json
import os
import bcrypt
import time
import re
from authlogger import AuthLogger

logger: AuthLogger = AuthLogger()


def authorize_api_request(event, context) -> dict:
    response: dict = {"isAuthorized": False}
    logger.log_info("Event: {}".format(event))
    noauth = True if "x-noauth" in event["headers"].keys() else False
    try:
        if check_authorisation_token(event["headers"]["x-authorization"], noauth):
            response = {"isAuthorized": True}
        else:
            logger.log_error("Authentication failed", "Invalid token hash sent")
    except Exception as ex:
        logger.log_exception_error(
            str(type(ex).__name__), "Authentication method failed with error", str(ex.args), str(ex)
        )
    return response


def check_authorisation_token(token_hash_sent: str, noauth: bool) -> bool:
    client = boto3.client("secretsmanager")
    if noauth and os.environ.get("DRD_ALLOW_NO_AUTH", "False") == "True":
        logger.log_info("Noauth actioned as allowed")
        return True
    if not re.match(r"^\$2[by]\$(0[4-9]|1[012])\$[.\/0-9A-Za-z]{21}[.Oeu][.\/0-9A-Za-z]{31}$", token_hash_sent):
        return False
    secrets_response = client.get_secret_value(
        SecretId=os.environ["SECRET_STORE"],
    )
    secrets = json.loads(secrets_response["SecretString"])
    time_factor = str(int(time.time() / 1800))
    token = str(secrets["ROAD_DISTANCE_API_TOKEN"]) + time_factor
    return bcrypt.checkpw(token.encode("utf-8"), re.sub(r"^\$2y", "$2b", token_hash_sent).encode("utf-8"))
