# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: RequestsCommon.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="RequestsCommon.proto",
    package="com.igeolise.traveltime.rabbitmq.requests",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x14RequestsCommon.proto\x12)com.igeolise.traveltime.rabbitmq.requests""\n\x06\x43oords\x12\x0b'
    + b'\n\x03lat\x18\x01 \x01(\x02\x12\x0b\n\x03lng\x18\x02 \x01(\x02"]\n\x0eTransportation\x12K\n\x04type\x18'
    + b"\x01 \x01(\x0e\x32=.com.igeolise.traveltime.rabbitmq.requests.TransportationType*}\n\x12TransportationType"
    + b"\x12\x14\n\x10PUBLIC_TRANSPORT\x10\x00\x12\x0b\n\x07\x44RIVING\x10\x01\x12 \n\x1c"
    + b"\x44RIVING_AND_PUBLIC_TRANSPORT\x10\x02\x12\x15\n\x11\x44RIVING_AND_FERRY\x10\x03\x12\x0b\n\x07WALKING"
    + b"\x10\x04*!\n\nTimePeriod\x12\x13\n\x0fWEEKDAY_MORNING\x10\x00\x62\x06proto3",
)

_TRANSPORTATIONTYPE = _descriptor.EnumDescriptor(
    name="TransportationType",
    full_name="com.igeolise.traveltime.rabbitmq.requests.TransportationType",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PUBLIC_TRANSPORT",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="DRIVING",
            index=1,
            number=1,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="DRIVING_AND_PUBLIC_TRANSPORT",
            index=2,
            number=2,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="DRIVING_AND_FERRY",
            index=3,
            number=3,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="WALKING",
            index=4,
            number=4,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=198,
    serialized_end=323,
)
_sym_db.RegisterEnumDescriptor(_TRANSPORTATIONTYPE)

TransportationType = enum_type_wrapper.EnumTypeWrapper(_TRANSPORTATIONTYPE)
_TIMEPERIOD = _descriptor.EnumDescriptor(
    name="TimePeriod",
    full_name="com.igeolise.traveltime.rabbitmq.requests.TimePeriod",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name="WEEKDAY_MORNING",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=325,
    serialized_end=358,
)
_sym_db.RegisterEnumDescriptor(_TIMEPERIOD)

TimePeriod = enum_type_wrapper.EnumTypeWrapper(_TIMEPERIOD)
PUBLIC_TRANSPORT = 0
DRIVING = 1
DRIVING_AND_PUBLIC_TRANSPORT = 2
DRIVING_AND_FERRY = 3
WALKING = 4
WEEKDAY_MORNING = 0


_COORDS = _descriptor.Descriptor(
    name="Coords",
    full_name="com.igeolise.traveltime.rabbitmq.requests.Coords",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="lat",
            full_name="com.igeolise.traveltime.rabbitmq.requests.Coords.lat",
            index=0,
            number=1,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="lng",
            full_name="com.igeolise.traveltime.rabbitmq.requests.Coords.lng",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=67,
    serialized_end=101,
)


_TRANSPORTATION = _descriptor.Descriptor(
    name="Transportation",
    full_name="com.igeolise.traveltime.rabbitmq.requests.Transportation",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="type",
            full_name="com.igeolise.traveltime.rabbitmq.requests.Transportation.type",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=103,
    serialized_end=196,
)

_TRANSPORTATION.fields_by_name["type"].enum_type = _TRANSPORTATIONTYPE
DESCRIPTOR.message_types_by_name["Coords"] = _COORDS
DESCRIPTOR.message_types_by_name["Transportation"] = _TRANSPORTATION
DESCRIPTOR.enum_types_by_name["TransportationType"] = _TRANSPORTATIONTYPE
DESCRIPTOR.enum_types_by_name["TimePeriod"] = _TIMEPERIOD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Coords = _reflection.GeneratedProtocolMessageType(
    "Coords",
    (_message.Message,),
    {
        "DESCRIPTOR": _COORDS,
        "__module__": "RequestsCommon_pb2"
        # @@protoc_insertion_point(class_scope:com.igeolise.traveltime.rabbitmq.requests.Coords)
    },
)
_sym_db.RegisterMessage(Coords)

Transportation = _reflection.GeneratedProtocolMessageType(
    "Transportation",
    (_message.Message,),
    {
        "DESCRIPTOR": _TRANSPORTATION,
        "__module__": "RequestsCommon_pb2"
        # @@protoc_insertion_point(class_scope:com.igeolise.traveltime.rabbitmq.requests.Transportation)
    },
)
_sym_db.RegisterMessage(Transportation)


# @@protoc_insertion_point(module_scope)