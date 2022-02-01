import config as config
from common import Common
from main import RoadDistance


class TestContracts(Common):

    """
    contracts are defined in openapi3 specification
    and validated via jsonschema
    """

    road_distance = RoadDistance({})

    def test_css_to_lambda_contract_happy(self):
        json_content = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        assert self.road_distance.validate_against_schema(json_content, "local")

    def test_lambda_to_provider_contract_happy(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_happy.json")
        assert self.road_distance.validate_against_schema(json_content, "provider")

    def test_provider_to_lambda_contract_happy(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_response_happy.json")
        assert self.road_distance.validate_against_schema(json_content, "provider-response")

    def test_contract_css_to_lambda_bad_request(self):
        json_content = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID)
        assert not self.road_distance.validate_against_schema(json_content, "local")

    def test_contract_css_to_lambda_bad_reference(self):
        json_content = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_INVALID_REFERENCE)
        assert not self.road_distance.validate_against_schema(json_content, "local")

    def test_contract_lambda_to_provider_bad_request(self):
        json_content = self.fetch_json(self.road_distance.contracts["provider"] + "_invalid_missing_element.json")
        assert not self.road_distance.validate_against_schema(json_content, "provider")

    def test_contract_lambda_to_provider_bad_response(self):
        json_content = self.fetch_json(
            self.road_distance.contracts["provider"] + "_response_invalid_missing_element.json"
        )
        assert not self.road_distance.validate_against_schema(json_content, "provider-response")

    def test_contract_lambda_to_ccs_happy(self):
        json_content = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_RESPONSE_HAPPY)
        assert self.road_distance.validate_against_schema(json_content, "local-response")

    def test_contract_lambda_to_ccs_invalid_distance_fails(self):
        json_content = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_RESPONSE_INVALID_DISTANCE)
        assert not self.road_distance.validate_against_schema(json_content, "local-response")

    def test_contract_lambda_to_ccs_missing_transaction_id_fails(self):
        json_content = self.fetch_json(config.JSON_DOS_ROAD_DISTANCE_RESPONSE_MISSING_TRANSACTION_ID)
        assert not self.road_distance.validate_against_schema(json_content, "local-response")

    def fetch_json(self, file_name: str):
        return super().fetch_test_json(file_name)
