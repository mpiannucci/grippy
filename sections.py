import struct
import datetime


class BaseSection(object):

    _uint8 = struct.Struct(b'>B')
    _uint16 = struct.Struct(b'>H')
    _uint24 = struct.Struct(b'>HB')
    _uint32 = struct.Struct(b'>I')
    _uint64 = struct.Struct(b'>Q')

    def __init__(self, data, offset):
        self._length = self._uint32.unpack_from(data, offset)[0]
        self._data = data[offset:offset+self._length]
        self._section_num = int(self._data[5])

    @property
    def length(self):
        return self._length

    @property
    def section_number(self):
        return self._section_num

class IndicatorSection(BaseSection):

    _disciplines = {
        0: 'meteorological',
        1: 'hydrological',
        2: 'land surface',
        3: 'space',
        4: 'space',
        10: 'oceanographic',
        255: 'missing'
    }

    def __init__(self, data):
        self._length = 16
        self._section_num = 0
        self._data = data[0:self._length]

    @property
    def valid(self):
        return str(self._data[0:4].decode()) == 'GRIB'

    @property
    def discipline(self):
        dis_value = int(self._data[6])
        if dis_value in self._disciplines:
            return self._disciplines[dis_value]
        else:
            return 'unknown: ' + str(dis_value)

    @property
    def edition(self):
        return int(self._data[7])

    @property
    def total_length(self):
        return self._uint64.unpack_from(self._data, 8)[0]

class IdentificationSection(BaseSection):

    _reference_date_significances = {
        0: 'analysis',
        1: 'start of forecast',
        2: 'verifying time of forecast',
        3: 'observation time',
        255: 'missing'
    }

    _production_statuses = {
        0: 'operational',
        1: 'operational test',
        2: 'research',
        3: 're-analysis',
        4: 'TIGGE', 
        5: 'TIGGE test', 
        6: 's2s operational',
        7: 's2s test', 
        8: 'UERRA',
        9: 'UERRA test', 
        255: 'missing'
    }

    _data_types = {
        0: 'analysis',
        1: 'forecast', 
        2: 'analysis and forecast', 
        3: 'control forecast', 
        4: 'perturbed forecast',
        5: 'control and perturbed forecast', 
        6: 'processed satellite observations', 
        7: 'processed radar observations', 
        8: 'event probability', 
        192: 'experimental',
        255: 'missing'
    }

    @property
    def reference_date_significance(self):
        significance = int(self._data[11])
        if significance in self._reference_date_significances:
            return self._reference_date_significances[significance]
        else:
            return 'unknown: ' + str(significance)

    @property
    def reference_date(self):
        return datetime.datetime(self._uint16.unpack_from(self._data, 12)[0], int(self._data[14]), int(self._data[15]), int(self._data[16]), int(self._data[17]))

    @property
    def production_status(self):
        status = int(self._data[19])
        if status in self._production_statuses:
            return self._production_statuses[status]
        else:
            return 'unknown: ' + str(status)

    @property
    def data_type(self):
        data_type = int(self._data[20])
        if data_type in self._data_types:
            return self._data_types[data_type]
        else:
            return 'unknown: ' + str(data_type)


