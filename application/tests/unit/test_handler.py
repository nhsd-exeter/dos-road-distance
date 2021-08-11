import os
import json
import application.handler as handler

class TestHandler:

    json_path: str = "tests/unit/test_json/"
    os.environ["LOGGER"] = "Test"

    def test_valid_ccs_request(self):
        request = json.dumps(self.fetch_json("dos_road_distance_api_happy.json"))
        result = handler.process_road_distance_request(request, None)
        response = result['status_code']
        assert(response == 200)

    def test_invalid_ccs_request(self):
        request = json.dumps(self.fetch_json("dos_road_distance_api_happy.json"))
        result = handler.process_road_distance_request(request, None)
        response = result['status_code']
        assert(response == 500)

    def fetch_json(self, file_name: str):
        try:
            with open(self.json_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))
