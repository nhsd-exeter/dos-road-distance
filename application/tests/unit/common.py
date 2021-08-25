import json


class Common:

    JSON_DOS_ROAD_DISTANCE_HAPPY = "dos_road_distance_api_happy.json"
    JSON_DOS_ROAD_DISTANCE_INVALID = "dos_road_distance_api_invalid_missing_element.json"
    JSON_TRAVEL_TIME_ERROR_400 = "travel_time_api_error_400.json"
    JSON_TRAVEL_TIME_ERROR_401 = "travel_time_api_error_401.json"
    JSON_TRAVEL_TIME_ERROR_406 = "travel_time_api_error_406.json"
    JSON_TRAVEL_TIME_ERROR_413 = "travel_time_api_error_413.json"
    JSON_TRAVEL_TIME_ERROR_415 = "travel_time_api_error_415.json"
    JSON_TRAVEL_TIME_ERROR_422 = "travel_time_api_error_422.json"
    JSON_TRAVEL_TIME_ERROR_500 = "travel_time_api_error_500.json"
    JSON_TRAVEL_TIME_ERROR_503 = "travel_time_api_error_503.json"
    JSON_TRAVEL_TIME_ERROR_504 = "travel_time_api_error_504.json"
    JSON_TRAVEL_TIME_REQUEST_HAPPY = "travel_time_api_happy.json"
    JSON_TRAVEL_TIME_REQUEST_INVALID = "travel_time_api_invalid_missing_element.json"
    JSON_TRAVEL_TIME_RESPONSE_HAPPY = "travel_time_api_response_happy.json"
    JSON_TRAVEL_TIME_RESPONSE_INVALID = "travel_time_api_response_invalid_missing_element.json"

    json_path: str = "tests/unit/test_json/"
    proto_path: str = "tests/unit/test_proto/"

    def fetch_json(self, file_name: str):
        try:
            with open(self.json_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))

    def fetch_proto(self, file_name: str):
        try:
            with open(self.proto_path + file_name) as proto_file:
                return proto_file.read()
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))
