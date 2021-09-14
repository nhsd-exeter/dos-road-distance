import proto.traveltime.TimeFilterFastResponse_pb2 as TimeFilterFastResponse


class TravelTimeResponse:
    traveltimes = []
    distances = []
    response = TimeFilterFastResponse.TimeFilterFastResponse()

    def decode_response_proto(self, response_protobuf: bytes) -> dict:
        self.response.ParseFromString(response_protobuf)
        self.traveltimes = list(self.response.properties.travelTimes)
        self.distances = list(self.response.properties.distances)
        return {"travelTimes": self.traveltimes, "distances": self.distances}
