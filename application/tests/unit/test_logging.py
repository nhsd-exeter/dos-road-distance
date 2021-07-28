from application.provider import Provider
import pytest
import re


class TestLogging:

    """
    All logs will contain:
    road_distance_pilot|message=
    transaction id
    request id

    All error logs (request and response) will contain:
    http status code=###
    road_distance_pilot|error=' + error description

    YYYY/MM/DD 00:00:00.000000+0100|<info|debug|error>|lambda|<request_id>|<transaction_id>|roaddistancepilot|<request|response>|<success|fail>|<error=|message=>|<additional>
    """

    LOG_DATETIME = "(20[234]\d\/[01]\d\/[0123]\d \d{2}:\d{2}:\d{2}\.\d{6}\+\d{4})"
    LOG_INFO_PREFIX = "\|info\|lambda"
    LOG_DETAILS_STATUS = "\|([^|]+)\|([^|]+)\|roaddistancepilot\|system\|success\|message=([^|]*)"
    LOG_DETAILS_RAW = "\|([^|]+)\|roaddistancepilot\|(ccsrequest|providerrequest|providerresponse)|.*"
    LOG_FAILURE_PREFIX = "\|error\|lambda\|([^|]+)\|([^|]+)\|roaddistancepilot"
    LOG_CCS_FAILURE = "\|ccsrequest\|failed\|error=([^|]*)"
    LOG_PROVIDER_FAILURE = "\|providerresponse\|failed\|error=([^|]*)"
    LOG_PROVIDER_RESPONSE = "\|([^|]+)\|([^|]+)\|roaddistancepilot\|providerresponse\|success\|reference=([^|]*)\|unreachable=(yes|no)\|distance=([\d.]+)?"

    provider = provider()

    def test_status_log_success(self):
        rx = LOG_DATETIME + LOG_INFO_PREFIX + LOG_DETAILS_STATUS
        result = provider.format_status_log("This is a message")
        assert re.search(rx, result) != None

    def test_raw_log_success(self):
        rx = LOG_DATETIME + LOG_INFO_PREFIX + LOG_DETAILS_RAW
        result = provider.format_raw_log("This is a message")
        assert re.search(rx, result) != None

    def test_provider_response_success_per_destination(self):
        rx = LOG_DATETIME + LOG_INFO_PREFIX + LOG_PROVIDER_RESPONSE
        result = provider.format_provider_success_log("1000001", True, 1000)
        assert re.search(rx, result) != None
        result = provider.format_provider_success_log("1000001", False)
        assert re.search(rx, result) != None

    def test_provider_response_failure(self):
        rx = LOG_DATETIME + LOG_FAILURE_PREFIX + LOG_PROVIDER_FAILURE
        result = provider.format_provider_error_log("status_code=422|description=there was an error")
        assert re.search(rx, result) != None

    def test_ccs_response_failure(self):
        rx = LOG_DATETIME + LOG_FAILURE_PREFIX + LOG_CCS_FAILURE
        result = provider.format_ccs_error_log("status_code=422|description=there was an error")
        assert re.search(rx, result) != None
