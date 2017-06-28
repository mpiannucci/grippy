from helpers import _uint32


class BaseTemplate(object):
    grid_type = 3
    data_type = 7

    def __init__(self, type_, number, name, data):
        self._type = type_
        self._number = number
        self._name = name
        self._data = data

    @property
    def template_type(self):
        return self._type

    @property
    def template_number(self):
        return self._number

    @property
    def template_name(self):
        return self._name

class GridTemplate(BaseTemplate):

    _earth_shape = {
        0: 'Earth assumed spherical with radius = 6,367,470.0 m',
        1: 'Earth assumed spherical with radius specified (in m) by data producer',
        2: 'Earth assumed oblate spheriod with size as determined by IAU in 1965 (major axis = 6,378,160.0 m, minor axis = 6,356,775.0 m, f = 1/297.0)', 
        3: 'Earth assumed oblate spheriod with major and minor axes specified (in km) by data producer', 
        4: 'Earth assumed oblate spheriod as defined in IAG-GRS80 model (major axis = 6,378,137.0 m, minor axis = 6,356,752.314 m, f = 1/298.257222101)',
        5: 'Earth assumed represented by WGS84 (as used by ICAO since 1998) (Uses IAG-GRS80 as a basis)',
        6: 'Earth assumed spherical with radius = 6,371,229.0 m', 
        7: 'Earth assumed oblate spheroid with major and minor axes specified (in m) by data producer',
        8: 'Earth model assumed spherical with radius 6,371,200 m, but the horizontal datum of the resulting Latitude/Longitude field is the WGS84 reference frame', 
        9: 'Earth represented by the OSGB 1936 Datum, using the Airy_1830 Spheroid, the Greenwich meridian as 0 Longitude, the Newlyn datum as mean sea level, 0 height.', 
        255: 'missing'
    }

    _resolution_flags = {

    }

class LatitudeLongitudeGridTemplate(GridTemplate):

    def __init__(self, data):
        super(LatitudeLongitudeGridTemplate, self).__init__(self.grid_type, 0, 'Latitude Longitude', data)

    @property
    def earth_shape_value(self):
        return int(self._data[14])

    @property
    def earth_shape(self):
        shape = int(self._data[14])
        if shape in self._earth_shape:
            return self._earth_shape[shape]
        else:
            return 'unknown: ' + str(shape)

    @property
    def earth_radius_scale_factor(self):
        return int(self._data[15])

    @property
    def earth_radius_scaled_value(self):
        return _uint32.unpack_from(self._data, 16)[0]

    @property
    def earth_major_axis_scale_factor(self):
        return int(self._data[20])

    @property
    def earth_major_axis_scaled_value(self):
        return _uint32.unpack_from(self._data, 21)[0]

    @property
    def earth_minor_axis_scale_factor(self):
        return int(self._data[25])

    @property
    def earth_minor_axis_scaled_value(self):
        return _uint32.unpack_from(self._data, 26)[0]

    @property
    def parallel_point_count(self):
        return _uint32.unpack_from(self._data, 30)[0]

    @property
    def meridian_point_count(self):
        return _uint32.unpack_from(self._data, 34)[0]

    @property
    def start_latitude(self):
        return _uint32.unpack_from(self._data, 46)[0]

    @property
    def start_longitude(self):
        return _uint32.unpack_from(self._data, 50)[0]

    @property
    def resolution_component_flags(self):
        return self._data[54]

    @property
    def end_latitude(self):
        return _uint32.unpack_from(self._data, 55)[0]

    @property
    def end_longitude(self):
        return _uint32.unpack_from(self._data, 59)[0]

    @property
    def i_direction_increment(self):
        return _uint32.unpack_from(self._data, 63)[0]

    @property
    def j_direction_increment(self):
        return _uint32.unpack_from(self._data, 67)[0]

    @property
    def scanning_mode_flags(self):
        return self._data[71]

def find_template(template_type, number, data):
    if template_type == BaseTemplate.grid_type:
        if number == 0:
            return LatitudeLongitudeGridTemplate(data)
    elif template_type == BaseTemplate.data_type:
        return None
    return None

