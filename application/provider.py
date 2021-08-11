import os
import json
import uuid
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError


class Provider:

    request: dict = {}
    response: dict = {}
    options: dict = {}
    url: str = ""
    request_id: str = ""
    contracts_path: str = "openapi_schemas/json/"
    contracts: dict = {
        "provider": "travel_time_api",
        "local": "dos_road_distance_api",
        "provider-response": "travel_time_api_response",
    }

    def __init__(self, request):
        print(os.getcwd())
        self.request = request
        self.create_request_id()

    def create_request_id(self):
        self.request_id = uuid.uuid4()

    def validate_against_schema(self, json: dict, schema_name: str) -> bool:
        try:
            contract = self.fetch_json(self.contracts[schema_name] + ".json")
            validate(instance=json, schema=contract)
            return True
        except (ValidationError, SchemaError, Exception) as error:
            print(error)
            return False

    def fetch_json(self, file_name: str):
        try:
            with open(self.contracts_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print("Exception: Unable to open file " + self.contracts_path + file_name + ". {0}".format(ex))
