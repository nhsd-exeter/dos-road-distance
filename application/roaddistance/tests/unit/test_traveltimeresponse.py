import config as config
from common import Common
from traveltime_response import TravelTimeResponse


class TestTravelTimeResponse(Common):
    def test_decode_response_proto_valid(self):
        traveltime_response_data_bin = super().fetch_test_proto_bin(config.PROTO_TRAVEL_TIME_RESPONSE_HAPPY_BIN)
        traveltime_response_data = super().fetch_test_proto(config.PROTO_TRAVEL_TIME_RESPONSE_HAPPY)

        tt_response = TravelTimeResponse()
        tt_response_decoded = tt_response.decode_response_proto(traveltime_response_data_bin)
        print(tt_response_decoded)
        print(traveltime_response_data)
        print(str(tt_response.response))
        assert traveltime_response_data == str(tt_response.response)

    def test_decode_response_proto_invalid(self):
        traveltime_response_data_bin = super().fetch_test_proto_bin(config.PROTO_TRAVEL_TIME_RESPONSE_ERROR_4_BIN)

        tt_response = TravelTimeResponse()
        tt_response_decoded = tt_response.decode_response_proto(traveltime_response_data_bin)
        print(tt_response_decoded)
        assert tt_response_decoded == {"error": "SOURCE_NOT_IN_GEOMETRY"}
