# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: joystick_status.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='joystick_status.proto',
  package='dora',
  syntax='proto3',
  serialized_pb=_b('\n\x15joystick_status.proto\x12\x04\x64ora\x1a\x1fgoogle/protobuf/timestamp.proto\"\xc3\x01\n\x0eJoystickStatus\x12(\n\x04sent\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x07\x62uttons\x18\x02 \x03(\x0b\x32\x1b.dora.JoystickStatus.Button\x12\'\n\x04\x61xes\x18\x03 \x03(\x0b\x32\x19.dora.JoystickStatus.Axis\x1a\x19\n\x06\x42utton\x12\x0f\n\x07pressed\x18\x01 \x01(\x08\x1a\x15\n\x04\x41xis\x12\r\n\x05value\x18\x01 \x01(\x02\"e\n\x0bJoystickAck\x12(\n\x04sent\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08received\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestampb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_JOYSTICKSTATUS_BUTTON = _descriptor.Descriptor(
  name='Button',
  full_name='dora.JoystickStatus.Button',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pressed', full_name='dora.JoystickStatus.Button.pressed', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=212,
  serialized_end=237,
)

_JOYSTICKSTATUS_AXIS = _descriptor.Descriptor(
  name='Axis',
  full_name='dora.JoystickStatus.Axis',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='dora.JoystickStatus.Axis.value', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=239,
  serialized_end=260,
)

_JOYSTICKSTATUS = _descriptor.Descriptor(
  name='JoystickStatus',
  full_name='dora.JoystickStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sent', full_name='dora.JoystickStatus.sent', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buttons', full_name='dora.JoystickStatus.buttons', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='axes', full_name='dora.JoystickStatus.axes', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_JOYSTICKSTATUS_BUTTON, _JOYSTICKSTATUS_AXIS, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=260,
)


_JOYSTICKACK = _descriptor.Descriptor(
  name='JoystickAck',
  full_name='dora.JoystickAck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sent', full_name='dora.JoystickAck.sent', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='received', full_name='dora.JoystickAck.received', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=262,
  serialized_end=363,
)

_JOYSTICKSTATUS_BUTTON.containing_type = _JOYSTICKSTATUS
_JOYSTICKSTATUS_AXIS.containing_type = _JOYSTICKSTATUS
_JOYSTICKSTATUS.fields_by_name['sent'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_JOYSTICKSTATUS.fields_by_name['buttons'].message_type = _JOYSTICKSTATUS_BUTTON
_JOYSTICKSTATUS.fields_by_name['axes'].message_type = _JOYSTICKSTATUS_AXIS
_JOYSTICKACK.fields_by_name['sent'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_JOYSTICKACK.fields_by_name['received'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['JoystickStatus'] = _JOYSTICKSTATUS
DESCRIPTOR.message_types_by_name['JoystickAck'] = _JOYSTICKACK

JoystickStatus = _reflection.GeneratedProtocolMessageType('JoystickStatus', (_message.Message,), dict(

  Button = _reflection.GeneratedProtocolMessageType('Button', (_message.Message,), dict(
    DESCRIPTOR = _JOYSTICKSTATUS_BUTTON,
    __module__ = 'joystick_status_pb2'
    # @@protoc_insertion_point(class_scope:dora.JoystickStatus.Button)
    ))
  ,

  Axis = _reflection.GeneratedProtocolMessageType('Axis', (_message.Message,), dict(
    DESCRIPTOR = _JOYSTICKSTATUS_AXIS,
    __module__ = 'joystick_status_pb2'
    # @@protoc_insertion_point(class_scope:dora.JoystickStatus.Axis)
    ))
  ,
  DESCRIPTOR = _JOYSTICKSTATUS,
  __module__ = 'joystick_status_pb2'
  # @@protoc_insertion_point(class_scope:dora.JoystickStatus)
  ))
_sym_db.RegisterMessage(JoystickStatus)
_sym_db.RegisterMessage(JoystickStatus.Button)
_sym_db.RegisterMessage(JoystickStatus.Axis)

JoystickAck = _reflection.GeneratedProtocolMessageType('JoystickAck', (_message.Message,), dict(
  DESCRIPTOR = _JOYSTICKACK,
  __module__ = 'joystick_status_pb2'
  # @@protoc_insertion_point(class_scope:dora.JoystickAck)
  ))
_sym_db.RegisterMessage(JoystickAck)


# @@protoc_insertion_point(module_scope)
