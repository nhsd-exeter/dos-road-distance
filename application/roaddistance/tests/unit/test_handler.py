import os
import config as config
from common import Common
import handler as handler


class TestHandler(Common):

    log_path: str = "tests/unit/test_log/rd.log"
    os.environ["LOGGER"] = "Test"

    def test_valid_ccs_request(self):
        self.purge_test_logs()
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        response = handler.process_road_distance_request(request, None)
        assert response["status"] == 200
        assert "transactionid" in response
        assert "destinations" in response
        assert "unreachable" in response
        assert (response["destinations"].len() + response["unreachable"].len()) == request["destinations"].len()
        assert os.path.isfile(self.log_path)

    def test_invalid_ccs_request_returns_400_response_with_message(self):
        self.purge_test_logs()
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID)
        response = handler.process_road_distance_request(request, None)
        assert response["status"] == 400
        assert "transactionid" in response
        assert "message" in response
        assert response["transactionid"].len() == 0
        assert response["message"] == "'transactionid' is a required property"
        assert os.path.isfile(self.log_path)

    def test_invalid_log_name_raises_value_error(self):
        self.purge_test_logs()
        os.environ["LOGGER"] = "DoesNotExist"
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID)
        response = handler.process_road_distance_request(request, None)
        assert response["status"] == 502
        assert not os.path.isfile(self.log_path)
        del os.environ["LOGGER"]

    def purge_test_logs(self):
        if os.path.isfile(self.log_path):
            os.remove(self.log_path)

    def fetch_json(self, file_name: str) -> str:
        return super().fetch_test_json(file_name)
