import struct


_int8 = struct.Struct(b'>b')
_uint8 = struct.Struct(b'>B')
_int16 = struct.Struct(b'>h')
_uint16 = struct.Struct(b'>H')
_uint24 = struct.Struct(b'>HB')
_int32 = struct.Struct(b'>i')
_uint32 = struct.Struct(b'>I')
_uint64 = struct.Struct(b'>Q')
_float32 = struct.Struct(b'>f')
_float64 = struct.Struct(b'>d')