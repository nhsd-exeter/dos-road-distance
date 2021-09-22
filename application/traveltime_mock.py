"""
Provides mock responses in protobuf format using pre-existing files for requests and responses.
The files are specified by transaction ID
"""

from application.common import Common
import config as config


class TravelTimeMock(Common):
    request_path = "requests/"
    response_path = "responses/"
    status_code = 200
    content = b''
    files_format = "proto_{}_"
    files_by_count = {
        5: "proto_5_destinations.bin",
        50: "proto_50_destinations.bin",
        500: "proto_500_destinations.bin",
        1500: "proto_1500_destinations.bin",
        3000: "proto_3000_destinations.bin",
    }
    files_by_transaction_id = {
        "43c31af7-1f53-470f-9edc-fed8f447dc8f": "proto_5_destinations.bin",
        "8fcb792e-b914-434d-aa94-b2cb2de25f48": "proto_50_destinations.bin",
        "3bb4c6dd-9cad-4140-83c1-86d207fccb32": "proto_500_destinations.bin",
        "79d326c4-e29c-4c75-bedb-143c48dc717a": "proto_1500_destinations.bin",
        "c50904c9-18a4-49f0-811e-d63f7ea84900": "proto_3000_destinations.bin",
    }

    def post(self, request, transaction_id="", service_count=0):
        if service_count > 0 and service_count in self.files_by_count:
            print("MOCK Matched on count of " + str(service_count))
            self.content = super().fetch_mock_proto_bin(
                self.response_path
                + self.files_by_count[service_count]
            )
        elif transaction_id != "" and transaction_id in self.files_by_transaction_id:
            print("MOCK Matched on transaction ID of " + transaction_id)
            self.content = super().fetch_mock_proto_bin(
                self.response_path
                + self.files_by_transaction_id[transaction_id]
            )
        else:
            print("MOCK No match defaulting to 5")
            self.content = super().fetch_mock_proto_bin(self.response_path + self.files_by_count[5])
        return self
