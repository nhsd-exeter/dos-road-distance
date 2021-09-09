from main import RoadDistance


def process_road_distance_request(event, context):
    try:
        road_distance = RoadDistance(event)
        status_code = road_distance.process_request()
        body = {"statusCode": status_code, "message": "complete"}
    except Exception as e:
        status_code = 502
        body = {"statusCode": status_code, "error": repr(e)}

    return body
