import re
import uuid
import json
from jsonschema.exceptions import STRONG_MATCHES
import pytest
from application.rdlogger import RDLogger


class TestLogging:

    """
    All logs will contain:
    road_distance_pilot|message=
    transaction id
    request id

    All error logs (request and response) will contain:
    http status code=###
    road_distance_pilot|error=' + error description

    """

    STR_LOG_LAMBDA = "lambda"
    STR_LOG_CCSREQUEST = "ccsrequest"
    STR_LOG_PROVIDERREQUEST = "providerrequest"
    STR_LOG_PROVIDERRESPONSE = "providerresponse"

    LOG1_DATETIME = r"(20[234]\d\/[01]\d\/[0123]\d \d{2}:\d{2}:\d{2}\.(\d{6}\+\d{4}|\d{3}))"
    LOG2_INFO_PREFIX = r"\|INFO\|{}".format(STR_LOG_LAMBDA)
    LOG2_FAILURE_PREFIX = r"\|ERROR\|{}".format(STR_LOG_LAMBDA)
    LOG3_SECOND_PREFIX = r"\|([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})\|([a-z0-9]{8}-[a-z0-9]{4}"
    +r"-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}|)\|roaddistancepilot"
    LOG4_DETAILS_BASIC = r"\|([^\|]+)"
    LOG4_DETAILS_STATUS = r"\|system\|success\|message=([^\|]*)"
    LOG4_DETAILS_RAW = r"\|({}|{}|{})\|.*".format(STR_LOG_CCSREQUEST, STR_LOG_PROVIDERREQUEST, STR_LOG_PROVIDERRESPONSE)
    LOG4_CCS_FAILURE = r"\|{}\|failed\|statuscode=([^\|]*)|error=([^\|]*)".format(STR_LOG_CCSREQUEST)
    LOG4_PROVIDER_FAILURE = r"\|{}\|failed\|statuscode=([^\|]*)|error=([^\|]*)".format(STR_LOG_PROVIDERRESPONSE)
    LOG4_PROVIDER_RESPONSE = r"\|{}\|success\|reference=([^\|]*)\|unreachable=(yes|no)\|distance=([\d.]+)?".format(
        STR_LOG_PROVIDERRESPONSE
    )

    TEST_PAYLOAD = "This is a test payload/message"

    test_log_path: str = "./tests/unit/test_log/"
    test_log_file: str = "rd.log"
    json_path: str = "tests/unit/test_json/"
    request_id: str = str(uuid.uuid4())
    transaction_id: str = str(uuid.uuid4())
    rdlogger = RDLogger("Test", request_id, transaction_id)

    def __fetch_json(self, file_name: str):
        try:
            with open(self.json_path + file_name) as json_file:
                return str(json.load(json_file))
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))

    def test_basic_log_success(self):
        rx = self.LOG1_DATETIME + self.LOG2_INFO_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_DETAILS_BASIC
        self.rdlogger.purge()
        self.rdlogger.log(self.TEST_PAYLOAD)
        result = re.search(rx, self.rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None
        rx = self.LOG1_DATETIME + self.LOG2_FAILURE_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_DETAILS_BASIC
        self.rdlogger.purge()
        self.rdlogger.log(self.TEST_PAYLOAD, "error")
        result = re.search(rx, self.rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_status_log_success(self):
        rx = self.LOG1_DATETIME + self.LOG2_INFO_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_DETAILS_STATUS
        self.rdlogger.purge()
        self.rdlogger.log_formatted(self.TEST_PAYLOAD, "status")
        result = re.search(rx, self.rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_raw_log_success(self):
        rx = self.LOG1_DATETIME + self.LOG2_INFO_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_DETAILS_RAW
        self.rdlogger.purge()
        self.rdlogger.log_formatted(self.TEST_PAYLOAD, "ccs_request")
        result = re.search(rx, self.rdlogger.read_log_output())
        assert result is not None
        self.rdlogger.purge()
        self.rdlogger.log_formatted(self.TEST_PAYLOAD, "provider_request")
        result = re.search(rx, self.rdlogger.read_log_output())
        assert result is not None
        self.rdlogger.purge()
        self.rdlogger.log_formatted(self.TEST_PAYLOAD, "provider_response")
        result = re.search(rx, self.rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_provider_response_success_per_destination(self):
        rx = self.LOG1_DATETIME + self.LOG2_INFO_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_PROVIDER_RESPONSE
        self.rdlogger.purge()
        self.rdlogger.log_provider_success("1000001", "yes", "1000")
        result = re.search(rx, self.rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None
        self.rdlogger.purge()
        self.rdlogger.log_provider_success("1000001", "no")
        result = re.search(rx, self.rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_provider_response_failure(self):
        rx = self.LOG1_DATETIME + self.LOG2_FAILURE_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_PROVIDER_FAILURE
        self.rdlogger.purge()
        self.rdlogger.log_provider_error("422", "there was an error")
        result = re.search(rx, self.rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_ccs_request_failure(self):
        rx = self.LOG1_DATETIME + self.LOG2_FAILURE_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_CCS_FAILURE
        self.rdlogger.purge()
        self.rdlogger.log_ccs_error("422", "there was an error")
        result = re.search(rx, self.rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_content_raw_ccs_request(self):
        json_content = self.__fetch_json("dos_road_distance_api_happy.json")
        print(json_content)
        self.rdlogger.purge()
        self.rdlogger.log_formatted(json_content, "ccs_request")
        compare = "{}|".format(self.STR_LOG_CCSREQUEST) + json_content
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1

    def test_content_raw_provider_request(self):
        json_content = self.__fetch_json("travel_time_api_happy.json")
        print(json_content)
        self.rdlogger.purge()
        self.rdlogger.log_formatted(json_content, "provider_request")
        compare = "{}|".format(self.STR_LOG_PROVIDERREQUEST) + json_content
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1

    def test_content_raw_provider_response(self):
        json_content = self.__fetch_json("travel_time_api_response_happy.json")
        print(json_content)
        self.rdlogger.purge()
        self.rdlogger.log_formatted(json_content, "provider_response")
        compare = "{}|".format(self.STR_LOG_PROVIDERRESPONSE) + json_content
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1

    def test_content_provider_response_success_per_destination(self):
        self.rdlogger.purge()
        self.rdlogger.log_provider_success("1000001", "yes", "1000")
        compare = "{}|success|reference=1000001|unreachable=yes|distance=1000".format(self.STR_LOG_PROVIDERRESPONSE)
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1

    def test_content_provider_failure(self):
        json_content = self.__fetch_json("travel_time_api_error_500.json")
        print(json_content)
        self.rdlogger.purge()
        self.rdlogger.log_provider_error("500", json_content)
        compare = "{}|failed|statuscode=500|error=".format(self.STR_LOG_PROVIDERRESPONSE) + json_content
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = self.rdlogger.read_log_output().find(compare)
        print(result)
        assert result is not -1

    def test_invalid_log_name_raises_value_error(self):
        with pytest.raises(ValueError):
            RDLogger("DoesNotExist", self.request_id, self.transaction_id)
