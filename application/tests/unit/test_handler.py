import os
import json
import application.config as config
from application.common import Common
import application.handler as handler


class TestHandler(Common):

    log_path: str = "tests/unit/test_log/rd.log"
    os.environ["LOGGER"] = "Test"

    def test_valid_ccs_request(self):
        self.purge_test_logs()
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        response = handler.process_road_distance_request(request, None)
        assert response["statusCode"] == 200
        assert os.path.isfile(self.log_path)

    def test_invalid_ccs_request(self):
        self.purge_test_logs()
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID)
        response = handler.process_road_distance_request(request, None)
        assert response["statusCode"] == 500
        assert os.path.isfile(self.log_path)

    def test_invalid_log_name_raises_value_error(self):
        self.purge_test_logs()
        os.environ["LOGGER"] = "DoesNotExist"
        request = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID)
        response = handler.process_road_distance_request(request, None)
        assert response["statusCode"] == 500
        assert not os.path.isfile(self.log_path)

    def purge_test_logs(self):
        if os.path.isfile(self.log_path):
            os.remove(self.log_path)

    def fetch_json(self, file_name: str) -> str:
        return json.dumps(super().fetch_test_json(file_name))
