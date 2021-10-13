import boto3
import json
import os

client = boto3.client("secretsmanager")


def authorize_api_request(event, context):
    print("Event: {}".format(event))
    response = {
        "isAuthorized": False,
    }
    try:
        token = get_secret_token()
        if event["headers"]["x-authorization"] == token:
            response = {"isAuthorized": True}
    except Exception as e:
        print("Authentication method failed with error: {}".format(e))
    print("Response: {}".format(response))
    return response


def get_secret_token():
    secrets_response = client.get_secret_value(
        SecretId=os.environ["SECRET_STORE"],
    )
    secrets = json.loads(secrets_response["SecretString"])
    token = secrets["API_RD_TOKEN"]
    return token
