from json import json_dumps
from common import Common
from application.traveltime_request import TravelTimeRequest


class TestTravelTimeRequest(Common):
    def fetch_json(self, file_name: str):
        return json_dumps(super().fetch_json(file_name))

    tt_request = TravelTimeRequest()
