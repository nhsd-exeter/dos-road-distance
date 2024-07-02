import boto3
import json
import os
import bcrypt
import time
import re
from authlogger import AuthLogger

logger: AuthLogger = AuthLogger()

# this global var is used only for unit testing
token_cached: bool = False

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


def fetch_secret_token(current_window: str) -> str:
    global token_cached

    if os.environ.get("RD_WINDOW", "") == current_window:
        token_cached = True
        if os.environ.get("RD_TOKEN", "") != "":
            return os.environ["RD_TOKEN"]

    client = boto3.client("secretsmanager")
    secrets_response = client.get_secret_value(
        SecretId=os.environ["SECRET_STORE"],
    )
    secrets = json.loads(secrets_response["SecretString"])
    os.environ["RD_WINDOW"] = current_window
    token = str(secrets["ROAD_DISTANCE_API_TOKEN"])
    os.environ["RD_TOKEN"] = token
    token_cached = False
    return token


def check_authorisation_token(token_hash_sent: str, noauth: bool) -> bool:
    if noauth and os.environ.get("DRD_ALLOW_NO_AUTH", "False") == "True":
        logger.log_info("Noauth actioned as allowed")
        return True

    if not re.match(r"^\$2[by]\$(0[4-9]|1[012])\$[.\/0-9A-Za-z]{21}[.Oeu][.\/0-9A-Za-z]{31}$", token_hash_sent):
        return False

    time_x = str(int((time.time() - 900) / 900))
    time_y = str(int(time.time() / 900))
    token_hash_sent = re.sub(r"^\$2y", "$2b", token_hash_sent)

    rd_token = fetch_secret_token(time_y)

    token_x = rd_token + time_x
    token_y = rd_token + time_y

    token_hash_sent_encoded = token_hash_sent.encode("utf-8")
    if bcrypt.checkpw(token_y.encode("utf-8"), token_hash_sent_encoded) or bcrypt.checkpw(
        token_x.encode("utf-8"), token_hash_sent_encoded
    ):
        return True

    return False
