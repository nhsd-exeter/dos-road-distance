import os
import task.config as config
from task.main import RoadDistance
from task.common import Common
import task.proto.traveltime.TimeFilterFastResponse_pb2 as TimeFilterFastResponse


class TestTravelTimeResponse(Common):

    os.environ["LOGGER"] = "Test"
    road_distance = RoadDistance({})

    def test_response_valid(self):
        ccs_request: dict = self.__fetch_test_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        road_distance = RoadDistance(ccs_request)
        road_distance.logger.purge()
        self.road_distance.process_request()
        # provider_response = self.road_distance.get_response()
        compare = (
            "|"
            + self.road_distance.request_id
            + "|"
            + ccs_request["transactionid"]
            + "|roaddistancepilot|providerresponse|"
            + str(ccs_request)
        )
        result = self.road_distance.logger.read_log_output().find(compare)
        print(result)
        assert result is not -1
