import proto.traveltime.RequestsCommon_pb2 as RequestsCommon
import proto.traveltime.TimeFilterFastRequest_pb2 as TimeFilterFastRequest
import proto.traveltime.TimeFilterFastResponse_pb2 as TimeFilterFastResponse
import requests


def build_request_proto(origin: dict, destinations: list) -> bytes:
    request = TimeFilterFastRequest.TimeFilterFastRequest()

    coords = RequestsCommon.Coords()
    coords.lat = origin["lat"]
    coords.lng = origin["lng"]

    transportation = RequestsCommon.Transportation()
    transportation.type = RequestsCommon.TransportationType.DRIVING

    location_deltas = []
    for destination in destinations:
        delta_lat = round((destination["lat"] - origin["lat"]) * 100000)
        delta_lng = round((destination["lng"] - origin["lng"]) * 100000)
        location_deltas.append(delta_lat)
        location_deltas.append(delta_lng)

    properties = [request.DISTANCES]

    one_to_many = TimeFilterFastRequest.TimeFilterFastRequest().OneToMany()
    one_to_many.departureLocation.CopyFrom(coords)
    one_to_many.transportation.CopyFrom(transportation)
    one_to_many.locationDeltas[:] = location_deltas
    one_to_many.properties[:] = properties
    one_to_many.travelTime = 7200

    request.oneToManyRequest.CopyFrom(one_to_many)

    print("REQUEST:")
    print(request)
    try:
        fh = open("/tmp/proto_request.dump", "w")
        fh.write(str(request))
        fh.close()
        fh = open("/tmp/proto_request.bin", "wb")
        fh.write(request.SerializeToString())
        fh.close()
    except Exception as ex:
        exit(ex)
    return request.SerializeToString()


def send_request(request):
    endpoint = os.environ.get("DRD_ENDPOINT")
    basic_auth = os.environ.get("DRD_BASICAUTH")
    r = requests.post(url=endpoint, data=request, headers={
            "Authorization": basic_auth,
            "Content-type": "application/octet-stream",
            "Accept": "application/octet-stream"
        }
    )
    print(r.status_code)
    return r.content


def decode_response(response):
    message = TimeFilterFastResponse.TimeFilterFastResponse()
    message.ParseFromString(response)
    print(message)
    try:
        fh = open("/tmp/proto_response.bin", "wb")
        fh.write(response)
        fh.close()
        fh = open("/tmp/proto_response.dump", "w")
        fh.write(str(message))
        fh.close()
    except Exception as ex:
        exit(ex)
    if message.error.type > 0:
        error_type = message.ErrorType.Name(message.error.type)
        return {"travelTimes": [], "distances": [], "error": error_type}
    traveltimes = list(message.properties.travelTimes)
    distances = list(message.properties.distances)
    return {"travelTimes": traveltimes, "distances": distances}


origin = {'lat': 500.72179229048227, 'lng': -3.525942582444856}
destinations = [
    {'lat': 50.71731288843375, 'lng': -3.5389588298795496}
]

request = build_request_proto(origin, destinations)
response = send_request(request)
message = decode_response(response)

print("RESPONSE")
# print(type(message))
print(message)
