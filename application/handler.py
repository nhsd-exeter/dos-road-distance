import json
from application.main import RoadDistance


def process_road_distance_request(event, context):
    try:
        road_distance = RoadDistance(json.loads(event))
        status_code = road_distance.process_request()
    except Exception as ex:
        status_code = 500

    response = {
        "status_code": status_code,
    }

    return response
