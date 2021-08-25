import application.proto.traveltime.RequestsCommon_pb2 as RequestsCommon
import application.proto.traveltime.TimeFilterFastRequest_pb2 as TimeFilterFastRequest


class TravelTimeRequest:

    TRAVEL_TIME_MINUTES = 7200

    def build_request_proto(self, origin: dict, destinations: list):
        request = TimeFilterFastRequest.TimeFilterFastRequest()

        coords = RequestsCommon.Coords()
        coords.lat = origin["lat"]
        coords.lng = origin["lng"]

        transportation = RequestsCommon.Transportation()
        transportation.type = RequestsCommon.TransportationType.DRIVING

        locationDeltas = self.create_deltas(origin, destinations)

        properties = [request.DISTANCES]

        oneToMany = TimeFilterFastRequest.TimeFilterFastRequest().OneToMany()
        oneToMany.departureLocation.CopyFrom(coords)
        oneToMany.transportation.CopyFrom(transportation)
        oneToMany.locationDeltas[:] = locationDeltas
        oneToMany.properties[:] = properties
        oneToMany.travelTime = self.TRAVEL_TIME_MINUTES

        request.oneToManyRequest.CopyFrom(oneToMany)

        return request.SerializeToString()

    def create_deltas(self, origin: dict, destinations: list) -> list:
        deltas = []
        for destination in destinations:
            deltaLat = round((destination["lat"] - origin["lat"]) * 100000)
            deltaLng = round((destination["lng"] - origin["lng"]) * 100000)
            deltas.append(deltaLat)
            deltas.append(deltaLng)

        return deltas
