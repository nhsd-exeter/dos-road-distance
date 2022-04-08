# Logger
Logging = {"Audit": {"Path": ""}, "Test": {"Path": "tests/unit/test_log/rd.log"}}

# Contract file names (excluding extension)
Contracts = {
    "local": "dos_road_distance_api",
    "local-response": "dos_road_distance_api_response",
    "local-response-400": "dos_road_distance_api_response_400",
    "local-response-500": "dos_road_distance_api_response_500",
    "provider": "travel_time_api",
    "provider-response": "travel_time_api_response",
}

# File paths
PATH_TEST_JSON = "tests/unit/test_json/"
PATH_TEST_PROTO = "tests/unit/test_proto/"
PATH_MOCK_PROTO = "mock/"

# Exception messages
EXCEPTION_FILE_CANNOT_BE_OPENED = "Exception: Unable to open file "
EXCEPTION_LOG_FORMATTER_NOT_FOUND = "Exception: Did not find a function for formatter "
EXCEPTION_LOG_NAME_NOT_FOUND = "Error: Logger name is not found "
EXCEPTION_DOS_ROADDISTANCE = "dos-road-distance exception: "

# Request and response files
JSON_DOS_ROAD_DISTANCE_HAPPY = "dos_road_distance_api_happy.json"
JSON_DOS_ROAD_DISTANCE_INVALID_JSON = "dos_road_distance_api_invalid_json.json"
JSON_DOS_ROAD_DISTANCE_RESPONSE_HAPPY = "dos_road_distance_api_response_happy.json"
JSON_DOS_ROAD_DISTANCE_RESPONSE_MISSING_TRANSACTION_ID = "dos_road_distance_api_response_missing_transaction_id.json"
JSON_DOS_ROAD_DISTANCE_RESPONSE_INVALID_DISTANCE = "dos_road_distance_api_response_invalid_distance.json"
JSON_DOS_ROAD_DISTANCE_HAPPY_SUPPRESSED = "dos_road_distance_api_happy_suppressed.json"
JSON_DOS_ROAD_DISTANCE_INVALID = "dos_road_distance_api_invalid_missing_element.json"
JSON_DOS_ROAD_DISTANCE_INVALID_REFERENCE = "dos_road_distance_api_invalid_reference.json"
JSON_DOS_ROAD_DISTANCE_INVALID_COORD = "dos_road_distance_api_invalid_coord.json"
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

PROTO_TRAVEL_TIME_REQUEST_HAPPY = "travel_time_proto_happy.dump"
PROTO_TRAVEL_TIME_REQUEST_HAPPY_BIN = "travel_time_proto_happy.bin"
PROTO_TRAVEL_TIME_REQUEST_ERROR_4 = "travel_time_proto_error_4.dump"
PROTO_TRAVEL_TIME_REQUEST_ERROR_4_BIN = "travel_time_proto_error_4.bin"
PROTO_TRAVEL_TIME_RESPONSE_HAPPY = "travel_time_proto_response_happy.dump"
PROTO_TRAVEL_TIME_RESPONSE_HAPPY_BIN = "travel_time_proto_response_happy.bin"
PROTO_TRAVEL_TIME_RESPONSE_ERROR_4 = "travel_time_proto_response_error_4.dump"
PROTO_TRAVEL_TIME_RESPONSE_ERROR_4_BIN = "travel_time_proto_response_error_4.bin"

MOCK_REQUEST_5_BIN = "proto_5_destinations.bin"
MOCK_REQUEST_50_BIN = "proto_50_destinations.bin"
MOCK_REQUEST_500_BIN = "proto_500_destinations.bin"
MOCK_REQUEST_1500_BIN = "proto_1500_destinations.bin"
MOCK_REQUEST_3000_BIN = "proto_3000_destinations.bin"
MOCK_REQUEST_VALID_CCS_REQUEST_BIN = "proto_valid_ccs_search.bin"
MOCK_REQUEST_A_SERVICE_WITHOUT_GRID_REFERENCES_BIN = "proto_a_service_without_grid_references.bin"
MOCK_REQUEST_ALL_DESTINATIONS_UNREACHABLE = "all_destinations_unreachable.bin"
MOCK_REQUEST_ERROR400_NO_SERVICES = "proto_error400_no_services.bin"
MOCK_REQUEST_ERROR400_BAD_REQUEST = "proto_error400_no_services.bin"
MOCK_REQUEST_ERROR500_INVALID_GRID_REFERENCE = "proto_error500_invalid_grid_reference.bin"

# TravelTime request and response values
TRAVEL_TIME_MINUTES = 7200
TRAVEL_TIME_DESTINATIONS_LIMIT = 3000
