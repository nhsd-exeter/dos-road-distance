import os
import json
import uuid
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from rdlogger import RDLogger
from common import Common
from traveltime_request import TravelTimeRequest
import config as config


class RoadDistance(Common):

    logger: RDLogger
    request: dict = {}
    response: dict = {}
    options: dict = {}
    url: str = ""
    status_code: int
    contracts_path: str = "openapi_schemas/json/"
    contracts: dict = config.Contracts
    request_id: str = ""

    def __init__(self, request):
        self.request = request
        transaction_id = str(self.request["transactionid"]) if "transactionid" in self.request else ""
        self.request_id = str(uuid.uuid4())
        log_name = os.environ.get("LOGGER", "Audit")
        self.logger = RDLogger(log_name, self.request_id, transaction_id)

    def process_request(self) -> int:
        if self.validate_against_schema(self.request, "local"):
            try:
                self.logger.log_formatted(str(self.request), "ccs_request")
                self.status_code = 200
            except Exception as ex:
                self.status_code = 500
                self.logger.log(config.LOG_CCS_REQUEST_EXCEPTION + str(ex), "error")
        else:
            self.status_code = 500
            self.logger.log_ccs_error(str(self.status_code), str(self.request))

        return self.status_code

    def build_request(self):
        origin = self.fetch_coords(self.request["origin"])
        destinations = self.fetch_destinations(self.request["destinations"])

        request = TravelTimeRequest()
        return request.build_request_proto(origin, destinations)

    def fetch_destinations(self, locations: list) -> list:
        destinations = []
        for location in locations:
            destinations.append(self.fetch_coords(location))

        return destinations

    def fetch_coords(self, location: dict) -> dict:
        return {"lat": location["latitude"], "lng": location["longitude"]}

    def validate_against_schema(self, json: dict, schema_name: str) -> bool:
        try:
            contract = self.fetch_json(self.contracts[schema_name] + ".json")
            validate(instance=json, schema=contract)
            return True
        except (ValidationError, SchemaError, Exception):
            return False

    def fetch_json(self, file_name: str) -> dict:
        try:
            return json.loads(super().fetch_file(self.contracts_path, file_name))
        except Exception as ex:
            self.logger.log(
                config.EXCEPTION_FILE_CANNOT_BE_OPENED + self.contracts_path + file_name + ". {0}".format(ex), "error"
            )
            raise ex
