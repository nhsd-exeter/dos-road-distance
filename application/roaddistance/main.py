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
    validation_error: str = ""

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

    def format_request_for_logging(self) -> str:
        copy = dict(self.request)
        exclusions = ["origin"]
        for exclusion in exclusions:
            copy.pop(exclusion, None)

        return str(copy)

    def process_request(self) -> dict:
        body: dict = {}
        try:
            if not self.validate_against_schema(self.request, "local"):
                body = self.process_validation_error()
            else:
                self.logger.log_formatted(self.format_request_for_logging(), "ccs_request")
                self.send_request(self.build_request())
                if not self.status_code == 200:
                    body = self.process_provider_response_error(self.response)
                else:
                    body = self.process_provider_response_success()
                    if len(self.request["destinations"]) != (len(self.destinations) + len(self.unreachable)):
                        raise RuntimeError("Mismatch of destinations in response, problem forming")
        except (Exception) as er:
            body = self.process_fatal_error(str(er))

        self.logger.log("CCS response body: " + str(body))
        return body

    def process_validation_error(self):
        self.status_code = 400
        self.logger.log_ccs_error(self.status_code, "Validation error", self.format_request_for_logging())
        return {
            "status": self.status_code,
            "message": "Validation error: " + self.validation_error,
            "transactionid": self.transaction_id,
        }

    def process_provider_response_success(self) -> dict:
        end_time = datetime.now().microsecond
        total_time = end_time - self.start_time
        self.logger.log(
            "Completed road distance request. end_time: " + str(end_time) + ", total_time: " + str(total_time)
        )
        self.form_response_destinations()
        return {
            "status": self.status_code,
            "message": "",
            "transactionid": self.transaction_id,
            "destinations": self.destinations,
            "unreachable": self.unreachable,
        }

    def process_provider_response_error(self, error_response: str) -> dict:
        error_response = error_response.replace("\n", "")

        self.logger.log_ccs_error(self.status_code, "Protobuf returned error in request: " + error_response)
        if str(self.status_code)[0] == "4":
            return {"status": 400, "message": error_response, "transactionid": self.transaction_id}
        else:
            return {"status": 500, "message": error_response}

    def process_fatal_error(self, error: str) -> dict:
        self.status_code = 500
        self.logger.log(config.EXCEPTION_DOS_ROADDISTANCE + error, "error")
        return {"status": 500, "message": error}

    def form_response_destinations(self) -> None:
        self.destinations = {}
        self.unreachable = []
        try:
            for i in range(len(self.request["destinations"])):
                distance = self.response["distances"][i]
                traveltime = self.response["travelTimes"][i]
                if traveltime == -1:
                    unreachable = "yes"
                    distance = 999
                    self.unreachable.append(self.request["destinations"][i]["reference"])
                else:
                    unreachable = "no"
                    self.destinations[self.request["destinations"][i]["reference"]] = distance
                self.logger.log_provider_success(
                    str(self.request["destinations"][i]["reference"]), unreachable, distance
                )
        except Exception:
            return None

    def send_request(self, request: bytes):
        endpoint = os.environ.get("DRD_ENDPOINT")
        basic_auth = os.environ.get("DRD_BASICAUTH")
        mock_mode = os.environ.get("DRD_MOCK_MODE")
        if mock_mode == "True":
            self.logger.log("MOCK MODE ENABLED")
            if self.transaction_id[0:5] == "mock-":
                self.logger.log("Processing by transaction id " + self.transaction_id[5:])
                r = TravelTimeMock().post(transaction_id=self.transaction_id[5:])
            else:
                self.logger.log("Processing by service count of " + len(self.request["destinations"]))
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
        self.status_code = r.status_code
        self.response = self.decode_response(r.content)
        if "error" in self.response:
            self.status_code = 400
            self.response = self.response["error"]
        self.logger.log("TravelTime decoded response: " + str(self.response))

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
        except (ValidationError, SchemaError) as ex:
            self.validation_error = str(ex).split("\n")[0]
            self.logger.log(config.EXCEPTION_DOS_ROADDISTANCE + self.validation_error, "error")
            return False

    def fetch_json(self, file_name: str) -> dict:
        try:
            return json.loads(super().fetch_file(self.contracts_path, file_name))
        except Exception as ex:
            self.logger.log(
                config.EXCEPTION_FILE_CANNOT_BE_OPENED + self.contracts_path + file_name + ". {0}".format(ex), "error"
            )
            raise ex
