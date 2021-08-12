import os
import json
from application.main import RoadDistance


class TestRoadDistance:

    road_distance = RoadDistance({})
    json_path: str = "tests/unit/test_json/"

    def test_error_responses_handled_gracefully(self):
        for file in sorted(os.listdir(self.json_path)):
            if file.lower().find("_error_") != -1:
                json_content = self.fetch_json(file)
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

    def fetch_json(self, file_name: str):
        try:
            with open(self.json_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))
