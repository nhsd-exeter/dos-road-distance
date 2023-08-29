from main import RoadDistance
import json
from json import JSONDecodeError


def process_road_distance_request(event, context):
    try:
        if "body" in event:
            event = json.loads(event["body"])
        road_distance = RoadDistance(event)
        body = road_distance.process_request()
    except JSONDecodeError as ex:
        status_code = 500
        body = {"status": status_code, "message": repr(ex)}
    except Exception as ex:
        status_code = 502
        body = {
            "status": status_code,
            "message": repr(ex),
            "log_stream_name": context.get("log_stream_name", ""),
            "log_group_name": context.get("log_group_name", ""),
            "invoked_function_arn": context.get("invoked_function_arn", ""),
            "aws_request_id": context.get("aws_request_id", ""),
            "memory_limit_in_mb": context.get("memory_limit_in_mb", ""),
        }

    return body
