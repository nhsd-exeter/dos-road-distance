"""
Provides mock responses in protobuf format using pre-existing files for requests and responses.
The files are specified by transaction ID
"""
from common import Common
import config
from time import sleep
from random import randrange
from bisect import bisect_left


class TravelTimeMock(Common):
    request_path = "requests/"
    response_path = "responses/"
    status_code = 200
    content = ""
    status_message = ""
    delay: float = 0
    files_by_count = {
        5: config.MOCK_REQUEST_5_BIN,
        50: config.MOCK_REQUEST_50_BIN,
        500: config.MOCK_REQUEST_500_BIN,
        1500: config.MOCK_REQUEST_1500_BIN,
        3000: config.MOCK_REQUEST_3000_BIN,
    }
    """
    transaction_id: response_file => service_count
    service_count must exist in self.server_delay
    """
    count_by_transaction_id = {
        "43c31af7-1f53-470f-9edc-fed8f447dc8f": [config.MOCK_REQUEST_5_BIN, 5],
        "8fcb792e-b914-434d-aa94-b2cb2de25f48": [config.MOCK_REQUEST_50_BIN, 50],
        "3bb4c6dd-9cad-4140-83c1-86d207fccb32": [config.MOCK_REQUEST_500_BIN, 500],
        "79d326c4-e29c-4c75-bedb-143c48dc717a": [config.MOCK_REQUEST_1500_BIN, 1500],
        "c50904c9-18a4-49f0-811e-d63f7ea84900": [config.MOCK_REQUEST_3000_BIN, 3000],
        "valid_ccs_request": [config.MOCK_REQUEST_VALID_CCS_REQUEST_BIN, 500],
        "a_service_without_grid_references": [config.MOCK_REQUEST_A_SERVICE_WITHOUT_GRID_REFERENCES_BIN, 5],
    }
    error_by_transaction_id = {
        "error500_invalid_grid_reference": config.MOCK_REQUEST_ERROR500_INVALID_GRID_REFERENCE,
        "error400_sample": config.MOCK_REQUEST_ERROR400_BAD_REQUEST,
    }
    server_delay = {
        -1: {"min": 68, "max": 99},
        0: {"min": 68, "max": 99},
        5: {"min": 68, "max": 99},
        50: {"min": 68, "max": 109},
        500: {"min": 80, "max": 119},
        1500: {"min": 90, "max": 129},
        3000: {"min": 100, "max": 149},
    }

    def post(self, transaction_id: str = "", service_count: int = -1):
        if service_count == 0:
            self.status_message = "MOCK Matched on count of 0"
            self.content = super().fetch_mock_proto_bin(self.response_path + config.MOCK_REQUEST_ERROR400_NO_SERVICES)
        elif service_count > 0 and service_count < 3001:
            if service_count in self.files_by_count:
                self.status_message = "MOCK Matched on count of " + str(service_count)
            else:
                service_sizes = list(self.files_by_count.keys())
                adjusted_count = service_sizes[bisect_left(service_sizes, service_count)]
                self.status_message = (
                    "MOCK From count of " + str(service_count) + " using adjusted count of " + str(adjusted_count)
                )
                service_count = adjusted_count
            self.content = super().fetch_mock_proto_bin(self.response_path + self.files_by_count[service_count])
        elif transaction_id != "":
            if transaction_id in self.count_by_transaction_id:
                self.status_message = "MOCK Matched on transaction ID of " + transaction_id
                self.content = super().fetch_mock_proto_bin(
                    self.response_path + self.count_by_transaction_id[transaction_id][0]
                )
                service_count = self.count_by_transaction_id[transaction_id][1]
            elif transaction_id == "error500_invalid_grid_reference":
                self.status_message = "MOCK Matched on invalid grid reference"
                raise ValueError("Value out of range: -4994928269")
            elif transaction_id in self.error_by_transaction_id:
                self.status_message = "MOCK Matched on error transaction ID of " + transaction_id
                self.content = super().fetch_mock_proto_bin(
                    self.response_path + self.error_by_transaction_id[transaction_id]
                )
            else:
                self.status_message = "MOCK Failed on transaction ID of " + transaction_id
        else:
            self.status_message = "MOCK No match, defaulting to 5"
            self.content = super().fetch_mock_proto_bin(self.response_path + self.files_by_count[5])
            service_count = 5

        self.delay = randrange(self.server_delay[service_count]["min"], self.server_delay[service_count]["max"]) / 1000
        sleep(self.delay)

        return self
