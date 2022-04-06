import proto.traveltime.RequestsCommon_pb2 as RequestsCommon
import proto.traveltime.TimeFilterFastRequest_pb2 as TimeFilterFastRequest
import proto.traveltime.TimeFilterFastResponse_pb2 as TimeFilterFastResponse
import requests
import os


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
    r = requests.post(
        url=endpoint,
        data=request,
        headers={
            "Authorization": basic_auth,
            "Content-type": "application/octet-stream",
            "Accept": "application/octet-stream",
        },
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


origin = {"lat": 52.695697, "lng": 1.3396}
destinations = [{
    'lat': 52.686824,
    'lng': 1.323555
}, {
    'lat': 52.66125,
    'lng': 1.328225
}, {
    'lat': 52.692047,
    'lng': 1.282034
}, {
    'lat': 52.66789,
    'lng': 1.300178
}, {
    'lat': 52.730762,
    'lng': 1.363255
}, {
    'lat': 52.641956,
    'lng': 1.341071
}, {
    'lat': 52.71676,
    'lng': 1.420684
}, {
    'lat': 52.652531,
    'lng': 1.280993
}, {
    'lat': 52.643625,
    'lng': 1.299479
}, {
    'lat': 52.643272,
    'lng': 1.298944
}, {
    'lat': 52.670098,
    'lng': 1.253831
}, {
    'lat': 52.637255,
    'lng': 1.337135
}, {
    'lat': 52.701869,
    'lng': 1.240804
}, {
    'lat': 52.643921,
    'lng': 1.285656
}, {
    'lat': 52.637178,
    'lng': 1.296874
}, {
    'lat': 52.632405,
    'lng': 1.319958
}, {
    'lat': 52.634248,
    'lng': 1.289706
}, {
    'lat': 52.637205,
    'lng': 1.278766
}, {
    'lat': 52.679249,
    'lng': 1.226086
}, {
    'lat': 52.634521,
    'lng': 1.276629
}, {
    'lat': 52.626316,
    'lng': 1.298746
}, {
    'lat': 52.631028,
    'lng': 1.28064
}, {
    'lat': 52.623967,
    'lng': 1.286835
}, {
    'lat': 52.624411,
    'lng': 1.280248
}, {
    'lat': 52.641066,
    'lng': 1.241739
}, {
    'lat': 52.6183,
    'lng': 1.296577
}, {
    'lat': 52.620732,
    'lng': 1.284465
}, {
    'lat': 52.626243,
    'lng': 1.261142
}, {
    'lat': 52.641924,
    'lng': 1.226797
}, {
    'lat': 52.631792,
    'lng': 1.240817
}, {
    'lat': 52.618664,
    'lng': 1.269518
}, {
    'lat': 52.681489,
    'lng': 1.196182
}, {
    'lat': 52.6458,
    'lng': 1.217235
}, {
    'lat': 52.63755,
    'lng': 1.449801
}, {
    'lat': 52.609702,
    'lng': 1.289149
}, {
    'lat': 52.622369,
    'lng': 1.241391
}, {
    'lat': 52.622669,
    'lng': 1.437022
}, {
    'lat': 52.637192,
    'lng': 1.217283
}, {
    'lat': 52.648844,
    'lng': 1.203795
}, {
    'lat': 52.791348,
    'lng': 1.253177
}, {
    'lat': 52.60256,
    'lng': 1.236594
}, {
    'lat': 52.793962,
    'lng': 1.250346
}, {
    'lat': 52.588105,
    'lng': 1.418033
}, {
    'lat': 52.576315,
    'lng': 1.337388
}, {
    'lat': 52.709131,
    'lng': 1.534423
}, {
    'lat': 52.572517,
    'lng': 1.34355
}, {
    'lat': 52.820065,
    'lng': 1.38334
}, {
    'lat': 52.820065,
    'lng': 1.38334
}, {
    'lat': 52.770038,
    'lng': 1.517525
}, {
    'lat': 52.76874,
    'lng': 1.526985
}, {
    'lat': 52.600901,
    'lng': 1.175729
}, {
    'lat': 52.640969,
    'lng': 1.548667
}, {
    'lat': 52.721248,
    'lng': 1.107291
}, {
    'lat': 52.559353,
    'lng': 1.23598
}, {
    'lat': 52.764223,
    'lng': 1.108074
}, {
    'lat': 52.53896,
    'lng': 1.25819
}, {
    'lat': 52.672794,
    'lng': 1.61366
}, {
    'lat': 52.862379,
    'lng': 1.247526
}, {
    'lat': 52.572176,
    'lng': 1.121665
}, {
    'lat': 52.535628,
    'lng': 1.47928
}, {
    'lat': 52.703766,
    'lng': 1.63909
}, {
    'lat': 52.567921,
    'lng': 1.113879
}, {
    'lat': 52.87544,
    'lng': 1.431265
}, {
    'lat': 52.659058,
    'lng': 1.0334
}, {
    'lat': 52.500626,
    'lng': 1.296263
}, {
    'lat': 52.674686,
    'lng': 1.685649
}, {
    'lat': 52.698578,
    'lng': 1.691315
}, {
    'lat': 52.491027,
    'lng': 1.229088
}, {
    'lat': 52.702326,
    'lng': 0.979176
}, {
    'lat': 52.927884,
    'lng': 1.306245
}, {
    'lat': 52.656592,
    'lng': 1.724077
}, {
    'lat': 52.647569,
    'lng': 1.72493
}, {
    'lat': 52.678309,
    'lng': 0.944176
}, {
    'lat': 52.683767,
    'lng': 0.942383
}, {
    'lat': 52.58146,
    'lng': 0.98743
}, {
    'lat': 52.85595,
    'lng': 1.036939
}, {
    'lat': 52.666121,
    'lng': 0.940694
}, {
    'lat': 52.584751,
    'lng': 1.698455
}, {
    'lat': 52.752311,
    'lng': 0.943019
}, {
    'lat': 52.619127,
    'lng': 1.725527
}, {
    'lat': 52.604758,
    'lng': 1.71853
}, {
    'lat': 52.605958,
    'lng': 1.726403
}, {
    'lat': 52.573323,
    'lng': 1.702402
}, {
    'lat': 52.606218,
    'lng': 1.729276
}, {
    'lat': 52.44971,
    'lng': 1.442974
}, {
    'lat': 52.939688,
    'lng': 1.214777
}, {
    'lat': 52.576566,
    'lng': 1.714819
}, {
    'lat': 52.914476,
    'lng': 1.116042
}, {
    'lat': 52.514861,
    'lng': 1.020755
}, {
    'lat': 52.577124,
    'lng': 1.727734
}, {
    'lat': 52.518451,
    'lng': 1.016107
}, {
    'lat': 52.428527,
    'lng': 1.229008
}, {
    'lat': 52.453288,
    'lng': 1.562886
}, {
    'lat': 52.628852,
    'lng': 0.894462
}, {
    'lat': 52.539418,
    'lng': 1.72458
}, {
    'lat': 52.403871,
    'lng': 1.297539
}, {
    'lat': 52.403127,
    'lng': 1.299689
}, {
    'lat': 52.49326,
    'lng': 1.731593
}, {
    'lat': 52.478072,
    'lng': 1.715177
}, {
    'lat': 52.839329,
    'lng': 0.867593
}, {
    'lat': 52.66125,
    'lng': 1.328225
}, {
    'lat': 52.66789,
    'lng': 1.300178
}, {
    'lat': 52.652531,
    'lng': 1.280993
}, {
    'lat': 52.643272,
    'lng': 1.298944
}, {
    'lat': 52.637178,
    'lng': 1.296874
}, {
    'lat': 52.637205,
    'lng': 1.278766
}, {
    'lat': 52.679249,
    'lng': 1.226086
}, {
    'lat': 52.626316,
    'lng': 1.298746
}, {
    'lat': 52.681489,
    'lng': 1.196182
}, {
    'lat': 52.6458,
    'lng': 1.217235
}, {
    'lat': 52.791348,
    'lng': 1.253177
}, {
    'lat': 52.709131,
    'lng': 1.534423
}, {
    'lat': 52.572517,
    'lng': 1.34355
}, {
    'lat': 52.820065,
    'lng': 1.38334
}, {
    'lat': 52.770038,
    'lng': 1.517525
}, {
    'lat': 52.640969,
    'lng': 1.548667
}, {
    'lat': 52.703766,
    'lng': 1.63909
}, {
    'lat': 52.674686,
    'lng': 1.685649
}, {
    'lat': 52.698578,
    'lng': 1.691315
}, {
    'lat': 52.656592,
    'lng': 1.724077
}, {
    'lat': 52.584751,
    'lng': 1.698455
}, {
    'lat': 52.604758,
    'lng': 1.71853
}, {
    'lat': 52.573323,
    'lng': 1.702402
}, {
    'lat': 52.606218,
    'lng': 1.729276
}, {
    'lat': 52.939688,
    'lng': 1.214777
}, {
    'lat': 52.576566,
    'lng': 1.714819
}, {
    'lat': 52.577124,
    'lng': 1.727734
}, {
    'lat': 52.403127,
    'lng': 1.299689
}, {
    'lat': 52.478072,
    'lng': 1.715177
}, {
    'lat': 52.482123,
    'lng': 1.756043
}, {
    'lat': 52.456916,
    'lng': 1.715485
}, {
    'lat': 52.722306,
    'lng': 0.790119
}, {
    'lat': 52.347634,
    'lng': 1.50792
}, {
    'lat': 52.648544,
    'lng': 0.690513
}, {
    'lat': 52.655577,
    'lng': 0.686691
}, {
    'lat': 52.778675,
    'lng': 0.662309
}, {
    'lat': 52.412444,
    'lng': 0.749246
}, {
    'lat': 52.589033,
    'lng': 0.509114
}, {
    'lat': 52.48268,
    'lng': 0.527056
}, {
    'lat': 52.939772,
    'lng': 0.493074
}, {
    'lat': 52.626316,
    'lng': 1.298746
}, {
    'lat': 52.820065,
    'lng': 1.38334
}, {
    'lat': 52.561672,
    'lng': 1.71798
}, {
    'lat': 52.454149,
    'lng': 1.562352
}, {
    'lat': 52.467859,
    'lng': 1.744671
}, {
    'lat': 52.420624,
    'lng': 0.74977
}, {
    'lat': 52.194685,
    'lng': 0.990419
}, {
    'lat': 52.194685,
    'lng': 0.990419
}, {
    'lat': 52.231662,
    'lng': 0.709176
}, {
    'lat': 52.231662,
    'lng': 0.709176
}, {
    'lat': 52.231662,
    'lng': 0.709176
}, {
    'lat': 52.626316,
    'lng': 1.298746
}, {
    'lat': 52.617567,
    'lng': 1.221195
}, {
    'lat': 52.923567,
    'lng': 1.30916
}, {
    'lat': 52.347634,
    'lng': 1.50792
}]

request = build_request_proto(origin, destinations)
response = send_request(request)
message = decode_response(response)

print("RESPONSE")
# print(type(message))
print(message)
