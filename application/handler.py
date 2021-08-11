import json
from application.provider import Provider

def process_road_distance_request(event, context):
    request = json.loads(event)
    provider = Provider(request)
    provider.process_request()
    response = {
        "status_code": provider.get_status_code(),
    }

    return response
