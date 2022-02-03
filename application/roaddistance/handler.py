from main import RoadDistance
import json


def process_road_distance_request(event, context):
    try:
        if "body" in event:
            event = json.loads(event["body"])
        road_distance = RoadDistance(event)
        body = road_distance.process_request()
    except Exception as e:
        status_code = 502
        body = {"status": status_code, "message": repr(e)}

    return body
