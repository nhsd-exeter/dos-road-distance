import re
import uuid
import pytest
import config as config
import time
from common import Common
from rdlogger import RDLogger


class TestLogging(Common):

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
    LOG3_ID = r"\|([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})"
    LOG3_SECOND_PREFIX = LOG3_ID + LOG3_ID + r"\|road_distance"
    LOG4_DETAILS_BASIC = r"\|([^\|]+)"
    LOG4_DETAILS_STATUS = r"\|system\|success\|message=([^\|]*)"
    LOG4_DETAILS_RAW = r"\|({}|{}|{})\|.*".format(STR_LOG_CCSREQUEST, STR_LOG_PROVIDERREQUEST, STR_LOG_PROVIDERRESPONSE)
    LOG4_CCS_FAILURE = r"\|{}\|failed\|statuscode=([^\|]*)|error=([^\|]+)|data=([^\|]*)".format(STR_LOG_CCSREQUEST)
    LOG4_PROVIDER_FAILURE = r"\|{}\|failed\|statuscode=([^\|]*)|error=([^\|]+)|data=([^\|]*)".format(
        STR_LOG_PROVIDERRESPONSE
    )
    LOG4_PROVIDER_RESPONSE = r"\|{}\|success\|reference=([^\|]*)\|unreachable=(yes|no)\|distance=([\d.]+)?".format(
        STR_LOG_PROVIDERRESPONSE
    )
    LOG_SYSTEM_TIME = (
        r"\|road_distance_lambda\|status=([^\|]*)|(lambda_execution_time|provider_execution_time)=[0-9]+[.][0-9]+"
    )

    TEST_PAYLOAD = "This is a test payload/message"

    request_id: str = str(uuid.uuid4())
    transaction_id: str = str(uuid.uuid4())

    def __fetch_json(self, file_name: str):
        return str(super().fetch_test_json(file_name))

    def test_basic_log_success(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        rx = self.LOG1_DATETIME + self.LOG2_INFO_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_DETAILS_BASIC
        rdlogger.purge()
        rdlogger.log(self.TEST_PAYLOAD)
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None
        rx = self.LOG1_DATETIME + self.LOG2_FAILURE_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_DETAILS_BASIC
        rdlogger.purge()
        rdlogger.log(self.TEST_PAYLOAD, "error")
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_status_log_success(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        rx = self.LOG1_DATETIME + self.LOG2_INFO_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_DETAILS_STATUS
        rdlogger.purge()
        rdlogger.log_formatted(self.TEST_PAYLOAD, "status")
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_log_system_time(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        rx = self.LOG_SYSTEM_TIME
        rdlogger.purge()
        rdlogger.log_system_time("complete", str(time.time()))
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_raw_log_success(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        rx = self.LOG1_DATETIME + self.LOG2_INFO_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_DETAILS_RAW
        rdlogger.purge()
        rdlogger.log_formatted(self.TEST_PAYLOAD, "ccs_request")
        result = re.search(rx, rdlogger.read_log_output())
        assert result is not None
        rdlogger.purge()
        rdlogger.log_formatted(self.TEST_PAYLOAD, "provider_request")
        result = re.search(rx, rdlogger.read_log_output())
        assert result is not None
        rdlogger.purge()
        rdlogger.log_formatted(self.TEST_PAYLOAD, "provider_response")
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_provider_response_success_per_destination(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        rx = self.LOG1_DATETIME + self.LOG2_INFO_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_PROVIDER_RESPONSE
        rdlogger.purge()
        rdlogger.log_provider_success("1000001", "no", 1000)
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None
        rdlogger.purge()
        rdlogger.log_provider_success("1000001", "yes", 0)
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_provider_response_failure(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        rx = self.LOG1_DATETIME + self.LOG2_FAILURE_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_PROVIDER_FAILURE
        rdlogger.purge()
        rdlogger.log_provider_error(422, self.TEST_PAYLOAD)
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_ccs_request_failure(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        rx = self.LOG1_DATETIME + self.LOG2_FAILURE_PREFIX + self.LOG3_SECOND_PREFIX + self.LOG4_CCS_FAILURE
        rdlogger.purge()
        rdlogger.log_ccs_error(422, self.TEST_PAYLOAD, "data example")
        result = re.search(rx, rdlogger.read_log_output())
        print(rx)
        print(result)
        assert result is not None

    def test_content_raw_ccs_request(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        json_content = self.__fetch_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        print(json_content)
        rdlogger.purge()
        rdlogger.log_formatted(json_content, "ccs_request")
        compare = "{}|".format(self.STR_LOG_CCSREQUEST) + json_content
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1

    def test_content_raw_provider_request(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        json_content = self.__fetch_json(config.JSON_TRAVEL_TIME_REQUEST_HAPPY)
        print(json_content)
        rdlogger.purge()
        rdlogger.log_formatted(json_content, "provider_request")
        compare = "{}|".format(self.STR_LOG_PROVIDERREQUEST) + json_content
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1

    def test_content_raw_provider_response(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        json_content = self.__fetch_json(config.JSON_TRAVEL_TIME_RESPONSE_HAPPY)
        print(json_content)
        rdlogger.purge()
        rdlogger.log_formatted(json_content, "provider_response")
        compare = "{}|".format(self.STR_LOG_PROVIDERRESPONSE) + json_content
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1

    def test_content_provider_response_success_per_destination(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        rdlogger.purge()
        rdlogger.log_provider_success("1000001", "yes")
        compare = "{}|success|reference=1000001|unreachable=yes|distance=|km=|miles=".format(
            self.STR_LOG_PROVIDERRESPONSE
        )
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1
        rdlogger.purge()
        rdlogger.log_provider_success("1000001", "no", 1000)
        compare = "{}|success|reference=1000001|unreachable=no|distance=1000|km=1.0|miles=0.6".format(
            self.STR_LOG_PROVIDERRESPONSE
        )
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1

    def test_content_provider_failure(self):
        rdlogger = RDLogger("Test", self.request_id, self.transaction_id)
        json_content = self.__fetch_json(config.JSON_TRAVEL_TIME_ERROR_500)
        print(json_content)
        rdlogger.purge()
        rdlogger.log_provider_error(500, self.TEST_PAYLOAD, json_content)
        compare = (
            "{}|failed|statuscode=500|error={}|data=".format(self.STR_LOG_PROVIDERRESPONSE, self.TEST_PAYLOAD)
            + json_content
        )
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1
        compare = "{}|".format(self.STR_LOG_LAMBDA) + self.request_id + "|" + self.transaction_id + "|"
        result = rdlogger.read_log_output().find(compare)
        print(result)
        assert result != -1

    def test_invalid_log_name_raises_value_error(self):
        with pytest.raises(ValueError):
            RDLogger("DoesNotExist", self.request_id, self.transaction_id)
