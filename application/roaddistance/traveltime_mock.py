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
    content = b""
    status_message = ""
    delay: float
    files_by_count = {
        5: config.MOCK_REQUEST_5_BIN,
        50: config.MOCK_REQUEST_50_BIN,
        500: config.MOCK_REQUEST_500_BIN,
        1500: config.MOCK_REQUEST_1500_BIN,
        3000: config.MOCK_REQUEST_3000_BIN,
    }
    count_by_transaction_id = {
        "43c31af7-1f53-470f-9edc-fed8f447dc8f": 5,
        "8fcb792e-b914-434d-aa94-b2cb2de25f48": 50,
        "3bb4c6dd-9cad-4140-83c1-86d207fccb32": 500,
        "79d326c4-e29c-4c75-bedb-143c48dc717a": 1500,
        "c50904c9-18a4-49f0-811e-d63f7ea84900": 3000,
    }
    server_delay = {
        5: {"min": 68, "max": 99},
        50: {"min": 68, "max": 109},
        500: {"min": 80, "max": 119},
        1500: {"min": 90, "max": 129},
        3000: {"min": 100, "max": 149},
    }

    def post(self, transaction_id="", service_count=0):
        if service_count > 0:
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
        elif transaction_id != "" and transaction_id in self.count_by_transaction_id:
            self.status_message = "MOCK Matched on transaction ID of " + transaction_id
            self.content = super().fetch_mock_proto_bin(
                self.response_path + self.files_by_count[self.count_by_transaction_id[transaction_id]]
            )
            service_count = self.count_by_transaction_id[transaction_id]
        else:
            self.status_message = "MOCK No match, defaulting to 5"
            self.content = super().fetch_mock_proto_bin(self.response_path + self.files_by_count[5])
            service_count = 5
        self.delay = randrange(self.server_delay[service_count]["min"], self.server_delay[service_count]["max"]) / 1000
        sleep(self.delay)
        return self