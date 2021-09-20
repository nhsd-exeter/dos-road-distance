import proto.traveltime.TimeFilterFastResponse_pb2 as TimeFilterFastResponse


file = "response.bin"
with open(file, 'rb') as f:
    message = TimeFilterFastResponse.TimeFilterFastResponse()
    message.ParseFromString(f.read())

print(type(message))
print(message)
