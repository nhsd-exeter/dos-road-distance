import os
import json
import uuid
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from application.rdlogger import RDLogger


class RoadDistance:

    logger: RDLogger = None
    request: dict = {}
    response: dict = {}
    options: dict = {}
    url: str = ""
    status_code: int
    contracts_path: str = "openapi_schemas/json/"
    contracts: dict = {
        "provider": "travel_time_api",
        "local": "dos_road_distance_api",
        "provider-response": "travel_time_api_response",
    }
    request_id: str = ""
    transaction_id: str = ""

    def __init__(self, request):
        self.request = request
        self.transaction_id = str(self.request["transactionid"]) if "transactionid" in self.request else ""
        self.request_id = str(uuid.uuid4())
        log_name = os.environ.get("LOGGER", "Audit")
        self.logger = RDLogger(log_name, self.request_id, self.transaction_id)

    def process_request(self) -> int:
        if self.validate_against_schema(self.request, "local"):
            try:
                self.logger.log_formatted(str(self.request), "ccs_request")
                # build json -> protobuf
                # send
                # handle response
                self.status_code = 200
            except Exception as ex:
                self.status_code = 500
                self.logger.log("dos-road-distance exception: " + str(ex), "error")
        else:
            self.status_code = 500
            self.logger.log_ccs_error(str(self.status_code), str(self.request))

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
            print("Exception: Unable to open file " + self.contracts_path + file_name + ". {0}".format(ex))
