from application.tests.unit.common import Common
from application.main import RoadDistance


class TestContracts(Common):

    """
    contracts are defined in openapi3 specification
    and validated via jsonschema
    """

    road_distance = RoadDistance({})

    def test_css_to_lambda_contract_happy(self):
        json_content = self.fetch_json("dos_road_distance_api_happy.json")
        assert self.road_distance.validate_against_schema(json_content, "local")

    def test_lambda_to_provider_contract_happy(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_happy.json")
        assert self.road_distance.validate_against_schema(json_content, "provider")

    def test_provider_to_lambda_contract_happy(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_response_happy.json")
        assert self.road_distance.validate_against_schema(json_content, "provider-response")

    def test_contract_css_to_lambda_bad_request(self):
        json_content = self.fetch_json("dos_road_distance_api_invalid_missing_element.json")
        assert not self.road_distance.validate_against_schema(json_content, "local")

    def test_contract_lambda_to_provider_bad_request(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_invalid_missing_element.json")
        assert not self.road_distance.validate_against_schema(json_content, "provider")

    def test_contract_lambda_to_provider_bad_response(self):
        json_content = self.fetch_json(
            self.road_distance.contracts["provider"] + "_response_invalid_missing_element.json"
        )
        assert not self.road_distance.validate_against_schema(json_content, "provider-response")

    def fetch_json(self, file_name: str):
        return super().fetch_json(file_name)
