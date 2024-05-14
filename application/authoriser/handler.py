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
    if noauth and os.environ.get("DRD_ALLOW_NO_AUTH", "False") == "True":
        logger.log_info("Noauth actioned as allowed")
        return True

    time_x = str(int((time.time() - 900) / 900))
    time_y = str(int(time.time() / 900))
    token_hash_sent_encoded = re.sub(r"^\$2y", "$2b", token_hash_sent).encode("utf-8")

    if os.environ.get("RD_API_TOKEN_X_SLOT", "") == time_x and os.environ.get("RD_API_TOKEN_Y_SLOT", "") == time_y:
        if os.environ.get("RD_API_TOKEN_X_TOKEN", "") == token_hash_sent or os.environ.get("RD_API_TOKEN_Y_TOKEN", "") == token_hash_sent:
            return True

    if not re.match(r"^\$2[by]\$(0[4-9]|1[012])\$[.\/0-9A-Za-z]{21}[.Oeu][.\/0-9A-Za-z]{31}$", token_hash_sent):
        return False

    client = boto3.client("secretsmanager")

    secrets_response = client.get_secret_value(
        SecretId=os.environ["SECRET_STORE"],
    )
    secrets = json.loads(secrets_response["SecretString"])
    token_x = (str(secrets["ROAD_DISTANCE_API_TOKEN"]) + time_x)
    token_y = (str(secrets["ROAD_DISTANCE_API_TOKEN"]) + time_y)

    if bcrypt.checkpw(token_y.encode("utf-8"), token_hash_sent_encoded) or bcrypt.checkpw(token_x.encode("utf-8"), token_hash_sent_encoded):
        os.environ["RD_API_TOKEN_X_SLOT"] = time_x
        os.environ["RD_API_TOKEN_X_TOKEN"] = token_x
        os.environ["RD_API_TOKEN_Y_SLOT"] = time_y
        os.environ["RD_API_TOKEN_Y_TOKEN"] = token_y

        return True

    return False

