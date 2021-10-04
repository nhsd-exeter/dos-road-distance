import proto.traveltime.TimeFilterFastResponse_pb2 as TimeFilterFastResponse


class TravelTimeResponse:
    traveltimes = []
    distances = []
    error: str = ""
    response = TimeFilterFastResponse.TimeFilterFastResponse()

    def decode_response_proto(self, response_protobuf: bytes) -> dict:
        self.response.ParseFromString(response_protobuf)
        if self.response.error.type > 0:
            error_type = str(self.response.ErrorType.Name(self.response.error.type))
            return {'travelTimes': [], 'distances': [], 'error': error_type}
        self.traveltimes = list(self.response.properties.travelTimes)
        self.distances = list(self.response.properties.distances)
        return {'travelTimes': self.traveltimes, 'distances': self.distances}
