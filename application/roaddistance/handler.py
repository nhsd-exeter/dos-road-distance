from main import RoadDistance
import json


def process_road_distance_request(event, context):
    try:
        if "body" in event:
            event = json.loads(event["body"])
        road_distance = RoadDistance(event)
        status_code = road_distance.process_request()
        body = {"statusCode": status_code}
    except Exception as e:
        status_code = 502
        body = {"statusCode": status_code, "error": repr(e)}

    return body
