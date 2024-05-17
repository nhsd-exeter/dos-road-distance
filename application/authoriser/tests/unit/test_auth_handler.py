import boto3
import json
import os
import handler
import bcrypt
from unittest.mock import patch
from datetime import datetime
import time  # so we can override time.time

class TestAuthHandler:

    log_path: str = "tests/unit/test_log/auth.log"
    os.environ["LOGGER"] = "Test"
    os.environ["SECRET_STORE"] = "uec-dos-rd-nonprod/deployment"

    def get_token(self, token_time: datetime = None) -> str:
        client = boto3.client("secretsmanager")
        secrets_response = client.get_secret_value(
            SecretId=os.environ["SECRET_STORE"],
        )
        secrets = json.loads(secrets_response["SecretString"])
        if token_time is not None:
            with patch("tests.unit.test_auth_handler.time.time", return_value=time.mktime(token_time.timetuple())):
                time_factor = str(int(time.time() / 900))
        else:
            time_factor = str(int(time.time() / 900))
        return bcrypt.hashpw(
            (secrets["ROAD_DISTANCE_API_TOKEN"] + time_factor).encode("utf-8"), bcrypt.gensalt()
        ).decode("UTF-8")

    def check_authorisation_token_for_time(self, token: str, token_time: datetime) -> None:
        with patch("handler.time.time", return_value=time.mktime(token_time.timetuple())):
            return handler.check_authorisation_token(token, False)

    # this simulates context supplied to the Lambda entrypoint

    def test_valid_check_authorisation_token_cached(self) -> None:
        token = self.get_token()
        authorised_state = handler.check_authorisation_token(token, False)
        assert authorised_state
        assert handler.cache_state == "UNCACHED"
        token = self.get_token()
        authorised_state = handler.check_authorisation_token(token, False)
        assert authorised_state
        assert handler.cache_state == "CACHED"

    def test_valid_check_authorisation_token(self) -> None:
        authorised_state = handler.check_authorisation_token(self.get_token(), False)
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

    def test_authorisation_token_outside_window(self) -> None:
        token = self.get_token(datetime(2023, 11, 28, 10, 1))
        assert not self.check_authorisation_token_for_time(token, datetime(2023, 11, 28, 10, 31))

    def test_authorisation_slot_2_validates_slot_1_token(self) -> None:
        token = self.get_token(datetime(2023, 11, 28, 10, 15))
        assert self.check_authorisation_token_for_time(token, datetime(2023, 11, 28, 10, 31))

    def test_authorisation_tokens_either_side_of_threshold(self) -> None:
        token = self.get_token(datetime(2023, 11, 28, 10, 29))
        assert self.check_authorisation_token_for_time(token, datetime(2023, 11, 28, 10, 31))

    def test_authorisation_slot_2_validates_slot_2_token(self) -> None:
        token = self.get_token(datetime(2023, 11, 28, 10, 30))
        assert self.check_authorisation_token_for_time(token, datetime(2023, 11, 28, 10, 44))
