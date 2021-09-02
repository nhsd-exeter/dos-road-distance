import os
import json
import pytest
import task.config as config
from task.common import Common
from task.main import RoadDistance


class TestRoadDistance(Common):

    os.environ["LOGGER"] = "Test"
    road_distance: RoadDistance

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
        self.__setup(json_content)
        status_code = self.road_distance.process_request()
        assert status_code == 200
        compare = (
            "|"
            + self.road_distance.request_id
            + "|"
            + json_content["transactionid"]
            + "|roaddistancepilot|ccsrequest|"
            + str(json_content)
        )
        result = self.road_distance.logger.read_log_output().find(compare)
        print("result: " + str(result))
        assert result is not -1

    def test_error_responses_handled_gracefully(self):
        self.__setup()
        for file in sorted(os.listdir(config.PATH_TEST_JSON)):
            if file.lower().find("_error_") != -1:
                json_content = self.__fetch_json(file)
                http_status = json_content["http_status"]

                try:
                    response = self.road_distance.format_response(json_content)
                    response_content = json.loads(response)

                    assert response_content["http_status"] == http_status
                    assert response_content["error_code"] is not None

                except ValueError as ve:
                    print(ve)
                    assert False
                except Exception as ex:
                    print(ex)
                    assert False

    def __setup(self, json={}):
        self.road_distance = RoadDistance(json)
        self.road_distance.logger.purge()

    def __fetch_json(self, file_name: str):
        return super().fetch_test_json(file_name)
