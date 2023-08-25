import os
import config
from common import Common
import handler


class TestHandler(Common):

    log_path: str = "tests/unit/test_log/rd.log"
    os.environ["LOGGER"] = "Test"

    # this simulates context supplied to the Lambda entrypoint
    context = {
        "invoked_function_arn": "Test ARN",
        "memory_limit_in_mb": "Test Memory",
        "aws_request_id": "Test ID",
        "log_group_name": "Test Group",
        "log_stream_name": "Test Stream",
    }

    def test_valid_ccs_request(self):
        self.purge_test_logs()
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        response = handler.process_road_distance_request(request, self.context)
        assert response["status"] == 200
        assert "transactionid" in response
        assert "destinations" in response
        assert "unreachable" in response
        assert (len(response["destinations"]) + len(response["unreachable"])) == len(request["destinations"])
        assert os.path.isfile(self.log_path)

    def test_invalid_json_raises_exception(self):
        json_file = super().fetch_file(config.PATH_TEST_JSON, config.JSON_DOS_ROAD_DISTANCE_INVALID_JSON)
        event = {"body": json_file}
        response = handler.process_road_distance_request(event, self.context)
        assert response["status"] == 500
        assert response["message"].find("JSONDecodeError") != -1

    def test_invalid_ccs_request_returns_400_response_with_message(self):
        self.purge_test_logs()
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID)
        response = handler.process_road_distance_request(request, self.context)
        assert response["status"] == 400
        assert "transactionid" in response
        assert "message" in response
        assert len(response["transactionid"]) == 0
        assert response["message"] == "Validation error: 'transactionid' is a required property"
        assert os.path.isfile(self.log_path)

    def test_invalid_log_name_raises_value_error(self):
        self.purge_test_logs()
        os.environ["LOGGER"] = "DoesNotExist"
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID)
        response = handler.process_road_distance_request(request, self.context)
        print(response)
        assert response["status"] == 502
        assert not os.path.isfile(self.log_path)
        assert response["log_stream_name"] == "Test Stream"
        assert response["log_group_name"] == "Test Group"
        assert response["invoked_function_arn"] == "Test ARN"
        assert response["aws_request_id"] == "Test ID"
        assert response["memory_limit_in_mb"] == "Test Memory"
        del os.environ["LOGGER"]

    def purge_test_logs(self):
        if os.path.isfile(self.log_path):
            os.remove(self.log_path)

    def fetch_json(self, file_name: str) -> dict:
        return super().fetch_test_json(file_name)
