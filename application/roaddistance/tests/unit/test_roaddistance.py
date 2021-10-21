import os
import pytest
import config as config
from common import Common
from main import RoadDistance


class TestRoadDistance(Common):

    road_distance: RoadDistance
    mock_mode = os.environ.get("DRD_MOCK_MODE")

    def test_missing_contract_logs_exception(self):
        self.__setup()
        with pytest.raises(Exception):
            self.road_distance.fetch_json("some_unknown_contract")

    def test_validate_against_schema_logs_error(self):
        self.__setup()
        tmp_local = self.road_distance.contracts["local"]
        self.road_distance.contracts["local"] = "some_unknown_contract"

        result = self.road_distance.validate_against_schema({}, "local")
        assert not result
        compare = "Unable to open file openapi_schemas/json/some_unknown_contract"
        log = self.road_distance.logger.read_log_output().find(compare)
        assert log is not -1
        self.road_distance.contracts["local"] = tmp_local

    def test_fetch_coords_successful(self):
        self.__setup()
        json_content: dict = self.__fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        result = self.road_distance.fetch_coords(json_content["origin"])
        assert isinstance(result, dict)
        assert "lat" in result
        assert "lng" in result

    def test_fetch_coords_invalid_location(self):
        self.__setup()
        with pytest.raises(Exception):
            json_content = {"transaction_id": "AAA-BBBB-CCCC-DDD", "lat": 2.34534535, "lng": -5.89457968}
            self.road_distance.coords(json_content["origin"])

    def test_fetch_destinations_successful(self):
        self.__setup()
        json_content: dict = self.__fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        destinations = self.road_distance.fetch_destinations(json_content["destinations"])
        assert isinstance(destinations, list)
        for destination in destinations:
            assert isinstance(destination, dict)
            assert "lat" in destination
            assert "lng" in destination

    def test_valid_request(self):
        json_content: dict = self.__fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        json_content_suppressed: dict = self.__fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY_SUPPRESSED)
        self.__setup(json_content)
        status_code = self.road_distance.process_request()
        assert status_code == 200
        compare = (
            "|"
            + self.road_distance.request_id
            + "|"
            + json_content["transactionid"]
            + "|road_distance|ccsrequest|"
            + str(json_content_suppressed)
        )
        result = self.road_distance.logger.read_log_output().find(compare)
        print("result: " + str(result))
        assert result is not -1

    @pytest.mark.skipif(mock_mode == "True", reason="requires DRD_MOCK_MODE to be not True")
    def test_protobuf_error_responses_handled(self):
        json_content: dict = self.__fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID_COORD)
        self.__setup(json_content)
        status_code = self.road_distance.process_request()
        print(status_code)
        assert status_code == 500
        compare = (
            "|"
            + self.road_distance.request_id
            + "|"
            + json_content["transactionid"]
            + "|road_distance|Protobuf returned error in request: SOURCE_NOT_IN_GEOMETRY"
        )
        print(compare)
        result = self.road_distance.logger.read_log_output().find(compare)
        assert result is not -1

    def __setup(self, json={}):
        os.environ["LOGGER"] = "Test"
        self.road_distance = RoadDistance(json)
        self.road_distance.logger.purge()

    def __fetch_json(self, file_name: str):
        return super().fetch_test_json(file_name)
