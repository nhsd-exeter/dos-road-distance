import os
import json
import uuid
import logging
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from google.protobuf.json_format import Parse

class Provider():

    request: dict = {}
    response: dict = {}
    options: dict = {}

    url: str = ''
    request_id: str = ''
    
    contracts_path: str = 'openapi_schemas/json/' # Path to the JSON contracts
    contracts: dict = { 
    # The contract file prefixes for provider request/response, and the Lamba (local) request.
        'provider': 'travel_time_api',
        'local': 'dos_road_distance_api',
        'provider-response': 'travel_time_api_response'
    }


    def __init__(self, request):
        print(os.getcwd())
        self.request = request
        self.create_request_id()


    def create_request_id(self):
        self.request_id = uuid.uuid4()


    # Validate the JSON against the schema
    def validate_against_schema(self, json: dict, schema_name: str) -> bool:
        try:
            contract = self.fetch_json(self.contracts[schema_name] + '.json')
            result = validate(instance=json, schema=contract)
            print(result)
            return True
        except (ValidationError, SchemaError, Exception) as error:
            print(error)
            return False


    def fetch_json(self, file_name: str):
        try:
            with open(self.contracts_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print('Exception: Unable to open file ' + self.contracts_path + file_name + '. {0}'.format(ex))
