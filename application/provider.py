import os
import json
import uuid
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from google.protobuf.json_format import Parse
from application.rdlogger import RDLogger


class Provider:

    logger: RDLogger = None
    request: dict = {}
    response: dict = {}
    options: dict = {}
    url: str = ""
    request_id: str = ""
    status_code: int = None
    contracts_path: str = "openapi_schemas/json/"
    contracts: dict = {
        "provider": "travel_time_api",
        "local": "dos_road_distance_api",
        "provider-response": "travel_time_api_response",
    }

    def __init__(self, request):
        self.request = request
        transaction_id = self.request['transactionid'] if 'transactionid' in self.request else None
        self.logger = RDLogger('./log/', uuid.uuid4(), transaction_id)

    def process_request(self) -> None:
        if self.validate_against_schema(self.request, "local"):
            try:
                self.logger.log_formatted(self.request, 'format_ccs_request')
                # build json -> protobuf
                # send
                # handle response
            except Exception as ex:
                self.status_code = 500
                self.logger.log('dos-road-distance exception: ' + str(ex), 'error')
        else:
            self.status_code = 500
            self.logger.log_ccs_error(self.status_code, self.request)

    def get_status_code(self) -> int:
        return self.status_code

    def validate_against_schema(self, json: dict, schema_name: str) -> bool:
        try:
            contract = self.fetch_json(self.contracts[schema_name] + ".json")
            validate(instance=json, schema=contract)
            return True
        except (ValidationError, SchemaError, Exception) as error:
            print(error)
            return False

    def fetch_json(self, file_name: str) -> dict:
        try:
            with open(self.contracts_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print("Exception: Unable to open file " + self.contracts_path + file_name + ". {0}".format(ex))git
