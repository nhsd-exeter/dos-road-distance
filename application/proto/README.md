# Profofbuf Message Definitions

These directories contains protobuf definitions (.proto files), and associated python classes, for individual API providers.

The Python classes are generated from the .proto files using the protoc library, and should not be edited directly.

## Dependencies

The protobuf library must be installed:

     brew install protobuf

If errors occur during installation try:

    brew upgrade protobuf

## Generating python classes

    protoc -I=. --python_out=.  /path/to/proto_files/•.proto

Re-generating the Python classes will only be required if there are changes to the protobuf definitions (.proto files), which would most likely mean wider changes to the application.
