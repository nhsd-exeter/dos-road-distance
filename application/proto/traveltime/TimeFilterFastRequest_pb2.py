# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: TimeFilterFastRequest.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
import proto.traveltime.RequestsCommon_pb2 as RequestsCommon__pb2

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="TimeFilterFastRequest.proto",
    package="com.igeolise.traveltime.rabbitmq.requests",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b"\n\x1bTimeFilterFastRequest.proto\x12)com.igeolise.traveltime.rabbitmq.requests\x1a"
    + b'\x14RequestsCommon.proto"\xaf\x04\n\x15TimeFilterFastRequest\x12\x64\n\x10oneToManyRequest\x18'
    + b"\x01 \x01(\x0b\x32J.com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany\x1a"
    + b"\x89\x03\n\tOneToMany\x12L\n\x11\x64\x65partureLocation\x18\x01 \x01(\x0b\x32"
    + b"\x31.com.igeolise.traveltime.rabbitmq.requests.Coords\x12\x16\n\x0elocationDeltas\x18\x02 \x03"
    + b"(\x11\x12Q\n\x0etransportation\x18\x03 \x01(\x0b\x32"
    + b"\x39.com.igeolise.traveltime.rabbitmq.requests.Transportation\x12P\n\x11\x61rrivalTimePeriod\x18"
    + b"\x04 \x01(\x0e\x32\x35.com.igeolise.traveltime.rabbitmq.requests.TimePeriod\x12\x12\n\ntravelTime"
    + b"\x18\x05 \x01(\x11\x12]\n\nproperties\x18\x06 \x03(\x0e\x32I.com.igeolise.traveltime.rabbitmq."
    + b'requests.TimeFilterFastRequest.Property"$\n\x08Property\x12\t\n\x05\x46\x41RES\x10\x00\x12'
    + b"\r\n\tDISTANCES\x10\x01\x62\x06proto3",
    dependencies=[
        RequestsCommon__pb2.DESCRIPTOR,
    ],
)


_TIMEFILTERFASTREQUEST_PROPERTY = _descriptor.EnumDescriptor(
    name="Property",
    full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.Property",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name="FARES",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="DISTANCES",
            index=1,
            number=1,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=620,
    serialized_end=656,
)
_sym_db.RegisterEnumDescriptor(_TIMEFILTERFASTREQUEST_PROPERTY)


_TIMEFILTERFASTREQUEST_ONETOMANY = _descriptor.Descriptor(
    name="OneToMany",
    full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="departureLocation",
            full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany.departureLocation",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
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
            name="locationDeltas",
            full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany.locationDeltas",
            index=1,
            number=2,
            type=17,
            cpp_type=1,
            label=3,
            has_default_value=False,
            default_value=[],
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
            name="transportation",
            full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany.transportation",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
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
            name="arrivalTimePeriod",
            full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany.arrivalTimePeriod",
            index=3,
            number=4,
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
        _descriptor.FieldDescriptor(
            name="travelTime",
            full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany.travelTime",
            index=4,
            number=5,
            type=17,
            cpp_type=1,
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
        _descriptor.FieldDescriptor(
            name="properties",
            full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany.properties",
            index=5,
            number=6,
            type=14,
            cpp_type=8,
            label=3,
            has_default_value=False,
            default_value=[],
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
    serialized_start=225,
    serialized_end=618,
)

_TIMEFILTERFASTREQUEST = _descriptor.Descriptor(
    name="TimeFilterFastRequest",
    full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="oneToManyRequest",
            full_name="com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.oneToManyRequest",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
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
    nested_types=[
        _TIMEFILTERFASTREQUEST_ONETOMANY,
    ],
    enum_types=[
        _TIMEFILTERFASTREQUEST_PROPERTY,
    ],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=97,
    serialized_end=656,
)

_TIMEFILTERFASTREQUEST_ONETOMANY.fields_by_name["departureLocation"].message_type = RequestsCommon__pb2._COORDS
_TIMEFILTERFASTREQUEST_ONETOMANY.fields_by_name["transportation"].message_type = RequestsCommon__pb2._TRANSPORTATION
_TIMEFILTERFASTREQUEST_ONETOMANY.fields_by_name["arrivalTimePeriod"].enum_type = RequestsCommon__pb2._TIMEPERIOD
_TIMEFILTERFASTREQUEST_ONETOMANY.fields_by_name["properties"].enum_type = _TIMEFILTERFASTREQUEST_PROPERTY
_TIMEFILTERFASTREQUEST_ONETOMANY.containing_type = _TIMEFILTERFASTREQUEST
_TIMEFILTERFASTREQUEST.fields_by_name["oneToManyRequest"].message_type = _TIMEFILTERFASTREQUEST_ONETOMANY
_TIMEFILTERFASTREQUEST_PROPERTY.containing_type = _TIMEFILTERFASTREQUEST
DESCRIPTOR.message_types_by_name["TimeFilterFastRequest"] = _TIMEFILTERFASTREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TimeFilterFastRequest = _reflection.GeneratedProtocolMessageType(
    "TimeFilterFastRequest",
    (_message.Message,),
    {
        "OneToMany": _reflection.GeneratedProtocolMessageType(
            "OneToMany",
            (_message.Message,),
            {
                "DESCRIPTOR": _TIMEFILTERFASTREQUEST_ONETOMANY,
                "__module__": "TimeFilterFastRequest_pb2"
                # @@protoc_insertion_point(class_scope:com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest.OneToMany)
            },
        ),
        "DESCRIPTOR": _TIMEFILTERFASTREQUEST,
        "__module__": "TimeFilterFastRequest_pb2"
        # @@protoc_insertion_point(class_scope:com.igeolise.traveltime.rabbitmq.requests.TimeFilterFastRequest)
    },
)
_sym_db.RegisterMessage(TimeFilterFastRequest)
_sym_db.RegisterMessage(TimeFilterFastRequest.OneToMany)


# @@protoc_insertion_point(module_scope)
