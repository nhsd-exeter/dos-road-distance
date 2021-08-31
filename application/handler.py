import json
from application.main import RoadDistance


def process_road_distance_request(event, context):
    try:
        road_distance = RoadDistance(event)
        status_code = road_distance.process_request()
        body = {}
    except Exception as e:
        status_code = 502
        body = {
            "statusCode": status_code,
            "error": repr(e)
        }

    response = {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

    return response
