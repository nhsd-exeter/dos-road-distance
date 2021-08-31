import json
from application.main import RoadDistance


def process_road_distance_request(event, context):
    try:
        road_distance = RoadDistance(event)
        status_code = road_distance.process_request()
    except Exception:
        status_code = 500

    response = {
        "statusCode": status_code,
    }

    return response
