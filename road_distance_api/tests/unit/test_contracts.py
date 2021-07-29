import os
import json
import pytest
from road_distance_api.provider import Provider


class TestContracts:

    print(os.getcwd())

    """
    contracts are defined in openapi3 specification
    and validated via jsonschema
    """

    provider = Provider({})
    jsonPath:str = 'tests/unit/test_json/'

    def test_css_to_lambda_contract_happy(self):
        json_content = self.fetch_json('dos_road_distance_api_happy.json')
        assert self.provider.validate_against_schema('local', json_content) == True

    def test_lambda_to_Provider_contract_happy(self):
        json_content = self.fetch_json(self.provider.contracts['provider'] + '_happy.json')
        assert self.provider.validate_against_schema('provider', json_content) == True

    def test_Provider_to_lambda_contract_happy(self):
        json_content = self.fetch_json(self.provider.contracts['provider'] + '_response_happy.json')
        assert self.provider.validate_against_schema('provider-response', json_content) == True

    def test_contract_css_to_lambda_bad_request(self):
        json_content = self.fetch_json('dos_road_distance_api_invalid_missing_element.json')
        assert self.provider.validate_against_schema('local', json_content) == False

    def test_contract_lambda_to_Provider_bad_request(self):
        json_content = self.fetch_json(self.provider.contracts['provider'] + '_invalid_missing_element.json')
        assert self.provider.validate_against_schema('provider', json_content) == False

    def test_contract_lambda_to_Provider_bad_response(self):
        json_content = self.fetch_json(self.provider.contracts['provider']+ '_response_invalid_missing_element.json')
        assert self.provider.validate_against_schema('provider-response', json_content) == False

    def fetch_json(self, file_name: str):
        try:
            with open(self.jsonPath + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print('Exception: Unable to open file ' + file_name + '. {0}'.format(ex))
