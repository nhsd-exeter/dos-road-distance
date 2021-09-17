import pytest
import task.config as config
from task.common import Common
from task.traveltime_request import TravelTimeRequest
from task.main import RoadDistance
import task.proto.traveltime.TimeFilterFastRequest_pb2 as TimeFilterFastRequest


class TestTravelTimeRequest(Common):

    travel_time_request = TravelTimeRequest()

    def test_proto_request_valid(self):
        ccs_request = super().fetch_test_json(config.JSON_DOS_ROAD_DISTANCE_HAPPY)
        road_distance = RoadDistance(ccs_request)

        origin = road_distance.fetch_coords(road_distance.request["origin"])
        destinations = road_distance.fetch_destinations(road_distance.request["destinations"])

        tt_binary = self.travel_time_request.build_request_proto(origin, destinations)
        tt_model = TimeFilterFastRequest.TimeFilterFastRequest()

        try:
            # test the request build is returning a 'bytes' type string
            tt_model.ParseFromString(tt_binary)
            assert isinstance(tt_model.oneToManyRequest, TimeFilterFastRequest.TimeFilterFastRequest().OneToMany)
            assert self.fetch_test_proto(config.PROTO_TRAVEL_TIME_REQUEST_HAPPY) == str(tt_model)
        except (UnicodeDecodeError, AttributeError):
            assert False

    def test_invalid_request_data_raises_exception(self):
        origin = {"latitude": 2.345648375, "longitude": -3.4356837}
        destinations = []
        with pytest.raises(Exception):
            self.tt_request.build_request_proto(origin, destinations)
