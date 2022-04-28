import boto3
import json
import os
import bcrypt
import time

client = boto3.client("secretsmanager")


def authorize_api_request(event, context) -> dict:
    print("Event: {}".format(event))
    response = {
        "isAuthorized": False,
    }
    try:
        try:
            noauth = True if event["headers"]["x-noauth"] else False
        except NameError:
            noauth = False
        if check_authorisation_token(event["headers"]["x-authorization"], noauth):
            response = {"isAuthorized": True}
    except Exception as e:
        print("Authentication method failed with error: {}".format(e))
    print("Response: {}".format(response))
    return response


def check_authorisation_token(token_hash_sent: str, noauth: bool) -> bool:
    if noauth and os.environ.get("DRD_ALLOW_NO_AUTH", False):
        return True
    secrets_response = client.get_secret_value(
        SecretId=os.environ["SECRET_STORE"],
    )
    secrets = json.loads(secrets_response["SecretString"])
    time_factor = str(int(time.time() / 1800))
    token = str(secrets["ROAD_DISTANCE_API_TOKEN"]) + time_factor
    return bcrypt.checkpw(token.encode("utf-8"), token_hash_sent.encode("utf-8"))
