import boto3
import json
import os
import handler
import bcrypt
import time


class TestAuthHandler:

    log_path: str = "tests/unit/test_log/auth.log"
    os.environ["LOGGER"] = "Test"
    os.environ["SECRET_STORE"] = "uec-dos-rd-nonprod/deployment"
    client = boto3.client("secretsmanager")
    secrets_response = client.get_secret_value(
        SecretId=os.environ["SECRET_STORE"],
    )
    secrets = json.loads(secrets_response["SecretString"])
    time_factor = str(int(time.time() / 1800))
    token = bcrypt.hashpw((secrets["ROAD_DISTANCE_API_TOKEN"] + time_factor).encode("utf-8"), bcrypt.gensalt()).decode(
        "UTF-8"
    )

    # this simulates context supplied to the Lambda entrypoint

    def test_valid_check_authorisation_token(self) -> None:
        authorised_state = handler.check_authorisation_token(self.token, False)
        assert authorised_state

    def test_invalid_check_authorisation_token(self) -> None:
        authorised_state = handler.check_authorisation_token("brokenToken", False)
        assert authorised_state is False

    def test_check_authorisation_token_allow_no_auth(self) -> None:
        os.environ["DRD_ALLOW_NO_AUTH"] = "True"
        authorised_state = handler.check_authorisation_token("brokenToken", True)
        assert authorised_state

    def test_check_authorisation_token_disallow_no_auth(self) -> None:
        os.environ["DRD_ALLOW_NO_AUTH"] = "False"
        authorised_state = handler.check_authorisation_token("brokenToken", True)
        assert authorised_state is False
