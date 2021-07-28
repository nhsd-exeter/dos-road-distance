import sys
sys.path.append("../..")
import os
import json
import pytest
from provider import Provider

class TestContracts:

    """
    contracts are defined in openapi3 specification
    and validated via jsonschema
    """

    provider = Provider({})
    jsonPath:str = 'test_json/'

    def test_css_to_lambda_contract_happy(self):
        assert self.provider.validate_against_schema('dos_road_distance_api', self.fetch_json('dos_road_distance_api_happy.json'))

    def test_lambda_to_Provider_contract_happy(self):
        assert self.provider.validate_against_schema(self.provider.contract_name, self.fetch_json(self.provider.contract_name + '_happy.json'))

    def test_Provider_to_lambda_contract_happy(self):
        assert self.provider.validate_against_schema(self.provider.contract_name, self.fetch_json(self.provider.contract_name + '_response_happy.json'))

    def test_contract_css_to_lambda_bad_request(self):
        json_content = self.fetch_json('dos_road_distance_api_invalid_missing_element.json')
        assert self.provider.validate_against_schema('dos_road_distance_api', json_content) == False

    def test_contract_lambda_to_Provider_bad_request(self):
        json_content = self.fetch_json(Provider.contract_name + '_invalid_missing_element.json')
        assert self.provider.validate_against_schema(self.provider.contract_name, json_content) == False

    def test_contract_lambda_to_Provider_bad_response(self):
        json_content = self.fetch_json(Provider.contract_name + '_response_invalid_missing_element.json')
        assert self.provider.validate_against_schema(self.provider.contract_name, json_content) == False

    def fetch_json(self, file_name: str):
        try:
            with open(self.jsonPath + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print('Exception: Unable to open file ' + file_name + '. {0}'.format(ex))
