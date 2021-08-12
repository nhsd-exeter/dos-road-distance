import os
import json
from application.main import RoadDistance
from application.rdlogger import RDLogger


class TestRoadDistance:

    road_distance = RoadDistance({})
    json_path: str = "tests/unit/test_json/"

    def test_valid_request(self):
        json_content: dict = self.__fetch_json("dos_road_distance_api_happy.json")
        road_distance = RoadDistance(json_content)
        rdlogger = RDLogger("Test", road_distance.request_id, json_content["transactionid"])
        rdlogger.purge()
        status_code = road_distance.process_request()
        assert status_code == 200
        compare = "ccsrequest|" + str(json_content)
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1
        rdlogger.purge()
        json_response: dict = self.road_distance.get_response()
        compare = (
            "|"
            + road_distance.request_id
            + "|"
            + json_content["transactionid"]
            + "|roaddistancepilot|providerresponse|"
            + str(json_response)
        )
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1

    def test_error_responses_handled_gracefully(self):
        for file in sorted(os.listdir(self.json_path)):
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

    def __fetch_json(self, file_name: str):
        try:
            with open(self.json_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))
