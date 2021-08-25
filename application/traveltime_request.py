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

        location_deltas = self.create_deltas(origin, destinations)

        properties = [request.DISTANCES]

        one_to_many = TimeFilterFastRequest.TimeFilterFastRequest().OneToMany()
        one_to_many.departureLocation.CopyFrom(coords)
        one_to_many.transportation.CopyFrom(transportation)
        one_to_many.locationDeltas[:] = location_deltas
        one_to_many.properties[:] = properties
        one_to_many.travelTime = self.TRAVEL_TIME_MINUTES

        request.oneToManyRequest.CopyFrom(one_to_many)

        return request.SerializeToString()

    def create_deltas(self, origin: dict, destinations: list) -> list:
        deltas = []
        for destination in destinations:
            delta_lat = round((destination["lat"] - origin["lat"]) * 100000)
            delta_lng = round((destination["lng"] - origin["lng"]) * 100000)
            deltas.append(delta_lat)
            deltas.append(delta_lng)

        return deltas
