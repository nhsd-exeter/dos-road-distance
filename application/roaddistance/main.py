import os
import json
import uuid
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from rdlogger import RDLogger
from common import Common
from traveltime_request import TravelTimeRequest
from traveltime_response import TravelTimeResponse
import config as config
import requests
from traveltime_mock import TravelTimeMock
from datetime import datetime


class RoadDistance(Common):

    logger: RDLogger
    request: dict = {}
    destinations = []
    response: dict = {}
    status_code = 0
    options: dict = {}
    url: str = ""
    status_code: int
    contracts_path: str = "openapi_schemas/json/"
    contracts: dict = config.Contracts
    request_id: str = ""
    transaction_id: str = ""
    start_time: int

    def __init__(self, request):
        self.request = request
        self.transaction_id = str(self.request["transactionid"]) if "transactionid" in self.request else ""
        self.request_id = str(uuid.uuid4())
        log_name = os.environ.get("LOGGER", "Audit")
        self.logger = RDLogger(log_name, self.request_id, self.transaction_id)

        self.start_time = datetime.now().microsecond

        self.logger.log(
            "Started road distance request. start_time: " + str(self.start_time),
        )

    def process_request(self) -> int:
        if not self.validate_against_schema(self.request, "local"):
            self.status_code = 500
            self.logger.log_ccs_error(str(self.status_code), "Validation error", str(self.request))
            return self.status_code

        try:
            self.logger.log_formatted(str(self.request), "ccs_request")
            self.send_request(self.build_request())
            if "error" in self.response and self.response["error"]:
                self.status_code = 500
                self.logger.log("Protobuf returned error in request: " + self.response["error"], "error")
            else:
                self.log_individual_service_responses()
                self.status_code = 200
        except Exception as ex:
            self.status_code = 500
            self.logger.log(config.EXCEPTION_DOS_ROADDISTANCE + str(ex), "error")

        return self.status_code

    def log_individual_service_responses(self):
        for i in range(len(self.request["destinations"])):
            distance = self.response["distances"][i]
            traveltime = self.response["travelTimes"][i]
            if traveltime == -1:
                unreachable = "yes"
                distance = 999
            else:
                unreachable = "no"
            self.logger.log_provider_success(str(self.request["destinations"][i]["reference"]), unreachable, distance)

    def send_request(self, request: bytes):
        endpoint = os.environ.get("DRD_ENDPOINT")
        basic_auth = os.environ.get("DRD_BASICAUTH")
        mock_mode = os.environ.get("DRD_MOCK_MODE")
        if mock_mode == "True":
            self.logger.log("MOCK MODE ENABLED")
            r = TravelTimeMock().post(
                transaction_id=self.transaction_id, service_count=len(self.request["destinations"])
            )
            self.logger.log(r.status_message + "; delay added: " + str(r.delay))
        else:
            r = requests.post(
                url=endpoint,
                data=request,
                headers={
                    "Authorization": basic_auth,
                    "Content-type": "application/octet-stream",
                    "Accept": "application/octet-stream",
                },
            )
        if r.status_code == 200:
            self.status_code = 200
            self.response = self.decode_response(r.content)
        else:
            self.status_code = 500
            self.logger.log_ccs_error(
                str(self.status_code), "Protobuf endpoint error, status code: " + str(r.status_code)
            )
            self.logger.log("Protobuf endpoint error, status code: " + str(r.status_code), "error")

    def build_request(self):
        origin = self.fetch_coords(self.request["origin"])
        destinations = self.fetch_destinations(self.request["destinations"])

        request = TravelTimeRequest()
        return request.build_request_proto(origin, destinations)

    def decode_response(self, content: bytes):
        message = TravelTimeResponse()
        response_decoded = message.decode_response_proto(content)
        if os.environ.get("DRD_LOG_RESPONSE_RAW") == "True":
            self.logger.log_formatted(str(message.response), "provider_response")
        return response_decoded

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
        except (ValidationError, SchemaError, Exception) as ex:
            self.logger.log(config.EXCEPTION_DOS_ROADDISTANCE + str(ex), "error")
            return False

    def fetch_json(self, file_name: str) -> dict:
        try:
            return json.loads(super().fetch_file(self.contracts_path, file_name))
        except Exception as ex:
            self.logger.log(
                config.EXCEPTION_FILE_CANNOT_BE_OPENED + self.contracts_path + file_name + ". {0}".format(ex), "error"
            )
            raise ex
