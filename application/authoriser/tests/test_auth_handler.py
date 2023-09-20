import os
import handler

class TestAuthHandler():

    log_path: str = "tests/unit/test_log/auth.log"
    os.environ["LOGGER"] = "Test"

    # this simulates context supplied to the Lambda entrypoint

    def test_valid_check_authorisation_token(self) -> None:
        authorised_state = handler.check_authorisation_token("token", False)
        assert authorised_state
