import json
from application.main import RoadDistance


class TestContracts:

    """
    contracts are defined in openapi3 specification
    and validated via jsonschema
    """

    road_distance = RoadDistance({})
    json_path: str = "tests/unit/test_json/"

    def test_css_to_lambda_contract_happy(self):
        json_content = self.fetch_json("dos_road_distance_api_happy.json")
        assert self.road_distance.validate_against_schema(json_content, "local") == True

    def test_lambda_to_provider_contract_happy(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_happy.json")
        assert self.road_distance.validate_against_schema(json_content, "provider") == True

    def test_provider_to_lambda_contract_happy(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_response_happy.json")
        assert self.road_distance.validate_against_schema(json_content, "provider-response") == True

    def test_contract_css_to_lambda_bad_request(self):
        json_content = self.fetch_json("dos_road_distance_api_invalid_missing_element.json")
        assert self.road_distance.validate_against_schema(json_content, "local") == False

    def test_contract_lambda_to_provider_bad_request(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_invalid_missing_element.json")
        assert self.road_distance.validate_against_schema(json_content, "provider") == False

    def test_contract_lambda_to_provider_bad_response(self):
        json_content = self.fetch_json(
            self.road_distance.contracts["provider"] + "_response_invalid_missing_element.json"
        )
        assert self.road_distance.validate_against_schema(json_content, "provider-response") == False

    def fetch_json(self, file_name: str):
        try:
            with open(self.json_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))
