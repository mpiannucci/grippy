import struct

_uint8 = struct.Struct(b'>B')
_uint16 = struct.Struct(b'>H')
_uint24 = struct.Struct(b'>HB')
_uint32 = struct.Struct(b'>I')
_int32 = struct.Struct(b'i')
_uint64 = struct.Struct(b'>Q')
_float32 = struct.Struct(b'>f')
_float64 = struct.Struct(b'>d')