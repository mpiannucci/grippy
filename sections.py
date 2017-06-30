from helpers import _uint8, _uint16, _uint32, _uint64
import datetime
import templates


class BaseSection(object):

    def __init__(self, data, offset):
        self._length = _uint32.unpack_from(data, offset)[0]
        self._data = data[offset:offset+self._length]
        self._section_num = _uint8.unpack_from(self._data, 4)[0]

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
        try:
            return str(self._data[0:4].decode()) == 'GRIB'
        except:
            return False

    @property
    def discipline_value(self):
        return _uint8.unpack_from(self._data, 6)[0]

    @property
    def discipline(self):
        return self._disciplines.get(self.discipline_value)

    @property
    def edition(self):
        return _uint8.unpack_from(self._data[7])

    @property
    def total_length(self):
        return _uint64.unpack_from(self._data, 8)[0]

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
        significance = _uint8.unpack_from(self._data, 11)[0]
        if significance in self._reference_date_significances:
            return self._reference_date_significances[significance]
        else:
            return 'unknown: ' + str(significance)

    @property
    def reference_date(self):
        return datetime.datetime(_uint16.unpack_from(self._data, 12)[0], _uint8.unpack_from(self._data, 14)[0], _uint8.unpack_from(self._data, 15)[0], _uint8.unpack_from(self._data, 16)[0], _uint8.unpack_from(self._data, 17)[0])

    @property
    def production_status(self):
        status = _uint8.unpack_from(self._data, 19)[0]
        if status in self._production_statuses:
            return self._production_statuses[status]
        else:
            return 'unknown: ' + str(status)

    @property
    def data_type(self):
        data_type = _uint8.unpack_from(self._data, 20)[0]
        if data_type in self._data_types:
            return self._data_types[data_type]
        else:
            return 'unknown: ' + str(data_type)

class LocalUseSection(BaseSection):

    @property
    def exists(self):
        return self.section_number == 2

class GridDefinitionSection(BaseSection):

    _grid_sources = {
        0: 'specified in code',
        1: 'predetermined',
        255: 'not applicable'
    }

    _number_list_interpretation = {
        0: 'no appended list',
        1: 'Numbers define number of points corresponding to full coordinate circles (i.e. parallels).  Coordinate values on each circle are multiple of the circle mesh, and extreme coordinate values given in grid definition may not be reached in all rows.',
        2: 'Numbers define number of points corresponding to coordinate lines delimited by extreme coordinate values given in grid definition which are present in each row.',
        3: 'Numbers define the actual latitudes for each row in the grid. The list of numbers are integer values of the valid latitudes in microdegrees (scale by 106) or in unit equal to the ratio of the basic angle and the subdivisions number for each row, in the same order as specified in the "scanning mode flag" (bit no. 2)',
        255: 'missing'
    }

    def __init__(self, data, offset):
        super(GridDefinitionSection, self).__init__(data, offset)

        self._template = templates.find_template(templates.BaseTemplate.grid_type, self.grid_definition_template_number, self._data)

    @property
    def grid_definition_source(self):
        source = _uint8.unpack_from(self._data, 5)[0]
        if source in self._grid_sources:
            return self._grid_sources[source]
        else:
            return 'unknown: ' + source

    @property
    def data_point_count(self):
        return _uint32.unpack_from(self._data, 6)[0]

    @property
    def optional_defining_number_count(self):
        return _uint8.unpack_from(self._data, 10)[0]

    @property
    def defining_number_interpretation(self):
        interp = _uint8.unpack_from(self._data, 11)[0]
        if interp in self._number_list_interpretation:
            return self._number_list_interpretation[interp]
        else:
            return 'unknown: ' + interp

    @property
    def grid_definition_template_number(self):
        return _uint16.unpack_from(self._data, 12)[0]

    @property
    def template(self):
        return self._template

class ProductDefinitionSection(BaseSection):

    def __init__(self, data, offset, discipline):
        super(ProductDefinitionSection, self).__init__(data, offset)

        self._template = templates.find_template(templates.BaseTemplate.product_type, self.product_definition_template_number, self._data, discipline)

    @property
    def coord_values_after_template(self):
        return _uint16.unpack_from(self._data, 5)[0]

    @property
    def product_definition_template_number(self):
        return _uint16.unpack_from(self._data, 7)[0]

    @property
    def template(self):
        return self._template

class DataRepresentationSection(BaseSection):

    def __init__(self, data, offset):
        super(DataRepresentationSection, self).__init__(data, offset)

        self._template = templates.find_template(templates.BaseTemplate.data_rep_type, self.data_representation_template_number, self._data)

    @property
    def data_point_count(self):
        return _uint32.unpack_from(self._data, 5)[0]

    @property
    def data_representation_template_number(self):
        return _uint16.unpack_from(self._data, 9)[0]

    @property
    def template(self):
        return self._template

class BitMapSection(BaseSection):

    def __init__(self, data, offset):
        super(BitMapSection, self).__init__(data, offset)

    @property
    def bitmap_indicator_value(self):
        return _uint8.unpack_from(self._data, 5)[0]

    @property
    def has_bitmap(self):
        return self.bitmap_indicator_value == 0

    @property
    def raw_bitmap_data(self):
        return self._data[6:]

    @property
    def all_bit_data(self):
        all_bits = []
        for byte in self.raw_bitmap_data:
            bits = [int(b) for b in bin(byte)[2:].rjust(8, '0')]
            all_bits += bits
        return all_bits

    @property
    def all_bit_truths(self):
        return [bool(b) for b in self.all_bit_data]

    @property
    def does_data_exist(self, index):
        return self.all_bit_truths[index]

class DataSection(BaseSection):

    def __init__(self, data, offset, data_template):
        super(DataSection, self).__init__(data, offset)

        self._data_representation_template = data_template

    @property
    def data_template(self):
        return self._data_representation_template

    @property
    def raw_data_array(self):
        return self._data[5:]


class EndSection(BaseSection):

    def __init__(self, data, offset):
        self._length = 4
        self._section_num = 8
        self._data = data[offset:offset+self._length]

    @property
    def valid(self):
        return str(self._data[0:4].decode()) == '7777'
