import boto3
import json
import os
import bcrypt

client = boto3.client("secretsmanager")


def authorize_api_request(event, context) -> dict:
    print("Event: {}".format(event))
    response = {
        "isAuthorized": False,
    }
    try:
        if check_authorisation_token(event["headers"]["x-authorization"]):
            response = {"isAuthorized": True}
    except Exception as e:
        print("Authentication method failed with error: {}".format(e))
    print("Response: {}".format(response))
    return response


def check_authorisation_token(token_hash_sent: str) -> bool:
    secrets_response = client.get_secret_value(
        SecretId=os.environ["SECRET_STORE"],
    )
    secrets = json.loads(secrets_response["SecretString"])
    token = secrets["API_RD_TOKEN"]
    return bcrypt.checkpw(token, token_hash_sent)
