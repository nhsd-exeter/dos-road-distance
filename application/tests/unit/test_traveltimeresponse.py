import os
from application.main import RoadDistance
from application.common import Common


class TestTravelTimeResponse(Common):

    JSON_DOS_ROAD_DISTANCE_HAPPY = "dos_road_distance_api_happy.json"
    os.environ["LOGGER"] = "Test"
    road_distance = RoadDistance({})

    def test_response_valid(self):
        json_content: dict = self.__fetch_test_json(self.JSON_DOS_ROAD_DISTANCE_HAPPY)
        self.road_distance.logger.purge()
        json_response: dict = self.road_distance.get_response()
        compare = (
            "|"
            + self.road_distance.request_id
            + "|"
            + json_content["transactionid"]
            + "|roaddistancepilot|providerresponse|"
            + str(json_response)
        )
        result = self.road_distance.logger.read_log_output().find(compare)
        print(result)
        assert result is not -1
