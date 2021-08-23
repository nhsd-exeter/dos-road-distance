import proto.traveltime.RequestsCommon_pb2 as RequestsCommon
import proto.traveltime.TimeFilterFastRequest_pb2 as TimeFilterFastRequest


request = TimeFilterFastRequest.TimeFilterFastRequest()

coords = RequestsCommon.Coords()
coords.lat = 50.72179229048227
coords.lng = -3.525942582444856
print("coords")
print(coords)

transportation = RequestsCommon.Transportation()
transportation.type = RequestsCommon.TransportationType.DRIVING
print("transportation")
print(transportation)

locationDeltas = [100, 50, -10, -100]
print("locationDeltas")
print(locationDeltas)

properties = [request.DISTANCES]
print("properties")
print(properties)

oneToMany = TimeFilterFastRequest.TimeFilterFastRequest().OneToMany()
oneToMany.departureLocation.CopyFrom(coords)
oneToMany.transportation.CopyFrom(transportation)
oneToMany.locationDeltas.extend(locationDeltas)
oneToMany.properties.extend(properties)
oneToMany.travelTime = 7200
print("oneToMany")
print(oneToMany)

request.oneToManyRequest.CopyFrom(oneToMany)

print("request")
print(request)
