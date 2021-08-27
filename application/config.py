Logging = {"Audit": {"Path": "log/rd.log"}, "Test": {"Path": "tests/unit/test_log/rd.log"}}

Contracts = {
    "local": "dos_road_distance_api",
    "provider": "travel_time_api",
    "provider-response": "travel_time_api_response",
}

# file paths
PATH_TEST_JSON = "tests/unit/test_json/"
PATH_TEST_PROTO = "tests/unit/test_proto/"

EXCEPTION_FILE_CANNOT_BE_OPENED = "Exception: Unable to open file "
EXCEPTION_LOG_FORMATTER_NOT_FOUND = "Exception: Did not find a function for formatter "
EXCEPTION_LOG_NAME_NOT_FOUND = "Error: Logger name is not found "

LOG_CCS_REQUEST_EXCPETION = "dos-road-distance exception: "

# test response and response files
JSON_DOS_ROAD_DISTANCE_HAPPY = "dos_road_distance_api_happy.json"
JSON_DOS_ROAD_DISTANCE_INVALID = "dos_road_distance_api_invalid_missing_element.json"
JSON_TRAVEL_TIME_REQUEST_HAPPY = "travel_time_api_happy.json"
JSON_TRAVEL_TIME_REQUEST_INVALID = "travel_time_api_invalid_missing_element.json"
JSON_TRAVEL_TIME_RESPONSE_HAPPY = "travel_time_api_response_happy.json"
JSON_TRAVEL_TIME_RESPONSE_INVALID = "travel_time_api_response_invalid_missing_element.json"

JSON_TRAVEL_TIME_ERROR_400 = "travel_time_api_error_400.json"
JSON_TRAVEL_TIME_ERROR_401 = "travel_time_api_error_401.json"
JSON_TRAVEL_TIME_ERROR_406 = "travel_time_api_error_406.json"
JSON_TRAVEL_TIME_ERROR_413 = "travel_time_api_error_413.json"
JSON_TRAVEL_TIME_ERROR_415 = "travel_time_api_error_415.json"
JSON_TRAVEL_TIME_ERROR_422 = "travel_time_api_error_422.json"
JSON_TRAVEL_TIME_ERROR_500 = "travel_time_api_error_500.json"
JSON_TRAVEL_TIME_ERROR_503 = "travel_time_api_error_503.json"
JSON_TRAVEL_TIME_ERROR_504 = "travel_time_api_error_504.json"

PROTO_TRAVEL_TIME_REQUEST_HAPPY = "traveltime_proto_happy.dump"

# travel time request and response values
TRAVEL_TIME_MINUTES = 7200
