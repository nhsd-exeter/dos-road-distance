import json
from application.main import RoadDistance

def process_road_distance_request(event, context):
    road_distance = RoadDistance(json.loads(event))
    response = {
        "status_code": road_distance.process_request(),
    }

    return response
