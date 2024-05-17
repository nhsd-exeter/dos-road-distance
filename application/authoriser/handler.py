import boto3
import json
import os
import bcrypt
import time
import re
from authlogger import AuthLogger

logger: AuthLogger = AuthLogger()

cache_state : str = ""

def authorize_api_request(event, context) -> dict:
    global cache_state

    response: dict = {"isAuthorized": False}
    logger.log_info("Event: {}".format(event))
    noauth = True if "x-noauth" in event["headers"].keys() else False
    try:
        if check_authorisation_token(event["headers"]["x-authorization"], noauth):
            response = {"isAuthorized": True}
        else:
            logger.log_error("Authentication failed", "Invalid token hash sent [" + cache_state + "]")
    except Exception as ex:
        logger.log_exception_error(
            str(type(ex).__name__), "Authentication method failed with error [", cache_state, "]", str(ex.args), str(ex)
        )
    return response

def check_authorisation_token(token_hash_sent: str, noauth: bool) -> bool:
    global cache_state

    client = boto3.client("secretsmanager")
    if noauth and os.environ.get("DRD_ALLOW_NO_AUTH", "False") == "True":
        logger.log_info("Noauth actioned as allowed")
        return True
    if not re.match(r"^\$2[by]\$(0[4-9]|1[012])\$[.\/0-9A-Za-z]{21}[.Oeu][.\/0-9A-Za-z]{31}$", token_hash_sent):
        return False

    if (os.environ.get('RD_AUTH_SECRET_STRING', "") != ''):
        secret_string = os.environ["RD_AUTH_SECRET_STRING"]
        cache_state = "CACHED"
    else:
        client = boto3.client("secretsmanager")
        secrets_response = client.get_secret_value(
            SecretId=os.environ["SECRET_STORE"],
        )
        secrets = json.loads(secrets_response["SecretString"])
        secret_string = str(secrets["ROAD_DISTANCE_API_TOKEN"])
        os.environ["RD_AUTH_SECRET_STRING"] = secret_string
        cache_state = "UNCACHED"

    token_x = (secret_string + str(int((time.time() - 900) / 900))).encode("utf-8")
    token_y = (secret_string + str(int(time.time() / 900))).encode("utf-8")
    token_hash_sent_encoded = re.sub(r"^\$2y", "$2b", token_hash_sent).encode("utf-8")
    return bcrypt.checkpw(token_y, token_hash_sent_encoded) or bcrypt.checkpw(token_x, token_hash_sent_encoded)

