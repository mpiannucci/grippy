from helpers import _uint8, _uint32, _uint16, _float32
from collections import namedtuple


class BaseTemplate(object):
    grid_type = 3
    product_type = 4
    data_rep_type = 5
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
        return _uint8.unpack_from(self._data, 14)[0]

    @property
    def earth_shape(self):
        shape = _uint8.unpack_from(self._data, 14)[0]
        if shape in self._earth_shape:
            return self._earth_shape[shape]
        else:
            return 'unknown: ' + str(shape)

    @property
    def earth_radius_scale_factor(self):
        return _uint8.unpack_from(self._data, 15)[0]

    @property
    def earth_radius_scaled_value(self):
        return _uint32.unpack_from(self._data, 16)[0]

    @property
    def earth_major_axis_scale_factor(self):
        return _uint8.unpack_from(self._data, 20)[0]

    @property
    def earth_major_axis_scaled_value(self):
        return _uint32.unpack_from(self._data, 21)[0]

    @property
    def earth_minor_axis_scale_factor(self):
        return _uint8.unpack_from(self._data, 25)[0]

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

class ProductTemplate(BaseTemplate):

    Product = namedtuple('Product', ['description', 'parameters'])
    Parameter = namedtuple('Parameter', ['parameter', 'units', 'abbrev'])

    _meteorological_products = {
        0: Product('Temperature', {
            0: Parameter('Temperature', 'K', 'TMP'),
            1: Parameter('Virtual Temperature', 'K', 'VTMP'),
            2: Parameter('Potential Temperature', 'K', 'POT'), 
            3: Parameter('Pseudo-Adiabatic Potential Temperature', 'K', 'EPOT'), 
            4: Parameter('Maximum Temperature', 'K', 'TMAX'),
            5: Parameter('Minimum Temperature', 'K', 'TMIN'), 
            6: Parameter('Dew Point Temperature', 'K', 'DPT'),
            7: Parameter('Dew Point Depression', 'K', 'DEPR'),
            8: Parameter('Lapse Rate', 'Km-1', 'LAPR'), 
            12: Parameter('Heat Index', 'K', 'HEATX'), 
            13: Parameter('Wind Chill Factor', 'K', 'WCF')
        }), 
        1: Product('Moisture', {

        }),
        2: Product('Momentum', {

        }), 
        3: Product('Mass', {

        }),
        4: Product('Short-wave radiation', {

        }),
        5: Product('Long-wave radiation', {

        }),
        6: Product('Cloud', {

        }), 
        7: Product('Thermodynamic Stability indicies', {

        }), 
        8: Product('Kinematic Stability indicies', {

        }), 
        9: Product('Temperature Probabilities', {

        }),
        10: Product('Moisture Probabilities', {

        }), 
        11: Product('Momentum Probabilities', {

        }), 
        12: Product('Mass Probabilities', {

        }), 
        13: Product('Aerosols', {

        }), 
        14: Product('Trace gases', {

        }), 
        15: Product('Radar', {

        }), 
        16: Product('Forecast Radar Imagery', {

        }), 
        17: Product('Electrodynamics', {

        }), 
        18: Product('Nuclear/radiology', {

        }), 
        19: Product('Physical atmospheric properties', {

        }), 
        20: Product('Atmospheric chemical Constituents', {

        }),
        190: Product('CCITT IA5 string', {

        }), 
        191: Product('Miscellaneous', {

        }), 
        192: Product('Covariance', {

        })
    }

    _hydrological_products = {
        0: Product('Hydrology basic products', {

        }), 
        1: Product('Hydrology probabilities', {

        }), 
        2: Product('Inland water and sediment properties', {

        })
    }

    _land_surface_products = {
        0: Product('Vegetation/Biomass', {

        }),
        1: Product('Agricultural/Aquacultural Special Products', {

        }), 
        2: Product('Transportation-related Products', {

        }), 
        3: Product('Soil Products', {

        }), 
        4: Product('Fire Weather Products', {

        }), 
        5: Product('Land Surface Products', {

        }),
    }

    _space_products = {
        0: Product('Image format products', {

        }), 
        1: Product('Quantitative products', {

        }), 
        2: Product('Cloud Properties', {

        }), 
        3: Product('Flight Rules Conditions', {

        }), 
        4: Product('Volcanic Ash', {

        }), 
        5: Product('Sea-surface Temperature', {

        }), 
        6: Product('Solar Radiation', {

        }), 
        192: Product('Forecast Satellite Imagery', {

        })
    }

    _space_weather_products = {
        0: Product('Temperature', {

        }), 
        1: Product('Momentum', {

        }), 
        2: Product('Charged Particle Mass and Number', {

        }), 
        3: Product('Electric and Magnetic Fields', {

        }), 
        4: Product('Energetic Particles', {

        }), 
        5: Product('Waves', {

        }), 
        6: Product('Solar Electromagnetic Emissions', {

        }), 
        7: Product('Terrestrial Electromagnetic Emissions', {

        }), 
        8: Product('Imagery', {

        }), 
        9: Product('Ion-Neutral Coupling', {

        })
    }

    _oceanographic_products = {
        0: Product('Waves', {
            0: Parameter('Wave Spectra 1', '-', 'WVSP1'), 
            1: Parameter('Wave Spectra 2', '-', 'WVSP2'),
            2: Parameter('Wave Spectra 3', '-', 'WVSP3'),
            3: Parameter('Significant Height of Combined Wind Waves and Swell', 'm', 'HTSGW'),
            4: Parameter('Direction of Wind Waves', 'degree', 'WVDIR'),
            5: Parameter('Significant Height of Wind Waves', 'm', 'WVHGT'),
            6: Parameter('Mean Period of Wind Waves', 's', 'WVPER'), 
            7: Parameter('Direction of Swell Waves', 'degree', 'SWDIR'), 
            8: Parameter('Significant Height of Swell Waves', 'm', 'SWELL'),
            9: Parameter('Mean Period of Swell Waves', 's', 'SWPER'),
            10: Parameter('Primary Wave Direction', 'degree', 'DIRPW'), 
            11: Parameter('Primary Wave Mean Period', 's', 'PERPW'),
            12: Parameter('Secondary Wave Direction', 'degree', 'DIRSW'), 
            13: Parameter('Secondary Wave Mean Period', 's', 'PERSW'),
            14: Parameter('Direction of Combined Wind Waves and Swell', 'degree', 'WWSDIR'),
            15: Parameter('Mean Period of Combined Wind Waves and Swell', 's', 'MWSPER'), 
            16: Parameter('Coefficient of Drag With Waves', '-', 'CDWW'),
            17: Parameter('Friction Velocity', 'ms-1', 'FRICV'),
            18: Parameter('Wave Stress', 'Nm-2', 'WSTR'),
            19: Parameter('Normalised Waves Stress', '-', 'NWSTR'),
            20: Parameter('Mean Square Slope of Waves', '-', 'MSSW'),
            21: Parameter('U-component Surface Stokes Drift', 'ms-1', 'USSD'),
            22: Parameter('V-component Surface Stokes Drift', 'ms-1', 'VSSD'), 
            23: Parameter('Period of Maximum Individual Wave Height', 's', 'PMAXWH'),
            24: Parameter('Maximum Individual Wave Height', 'm', 'MAXWH'),
            25: Parameter('Inverse Mean Wave Frequency', 's', 'IMWF'),
            26: Parameter('Inverse Mean Frequency of The Wind Waves', 's', 'IMFWW'),
            27: Parameter('Inverse Mean Frequency of The Total Swell', 's', 'IMFTSW'),
            28: Parameter('Mean Zero-Crossing Wave Period', 's', 'MZWPER'),
            29: Parameter('Mean Zero-Crossing Period of The Wind Waves', 's', 'MZPWW'),
            30: Parameter('Mean Zero-Crossing Period of The Total Swell', 's', 'MZPTSW'),
            31: Parameter('Wave Directional Width', '-', 'WDIRW'),
            32: Parameter('Directional Width of The Wind Waves', '-', 'DIRWWW'),
            33: Parameter('Directional Width of The Total Swell', '-', 'DIRWTS'),
            34: Parameter('Peak Wave Period', 's', 'PWPER'),
            35: Parameter('Peak Period of The Wind Waves', 's', 'PPERWW'),
            36: Parameter('Peak Period of The Total Swell', 's', 'PPERTS'),
            37: Parameter('Altimeter Wave Height', 'm', 'ALTWH'),
            38: Parameter('Altimeter Corrected Wave Height', 'm', 'ALCWH'),
            39: Parameter('Altimeter Range Relative Correction', '-', 'ALRRC'),
            40: Parameter('10 Metre Neutral Wind Speed Over Waves', 'ms-1', 'MNWSOW'),
            41: Parameter('10 Metre Wind Direction Over Waves', 'degree', 'MWDIRW'),
            42: Parameter('Wave Engery Spectrum', 'm-2 s rad-1', 'WESP'), 
            43: Parameter('Kurtosis of The Sea Surface Elevation Due to Waves', '-', 'KSSEW'),
            44: Parameter('Benjamin-Feir Index', '-', 'BENINX'),
            45: Parameter('Spectral Peakedness Factor', 's-1', 'SPFTR'),
            192: Parameter('Wave Steepness', 'porportion', 'WSTP'),
            192: Parameter('Wave Length', '-', 'WLENG')
        }), 
        1: Product('Currents', {

        }), 
        2: Product('Ice', {

        }), 
        3: Product('Surface Properties', {

        }), 
        4: Product('Sub-surface Properties', {

        }), 
        191: Product('Miscellaneous', {

        })
    }

    _products = {
        0: _meteorological_products, 
        1: _hydrological_products, 
        2: _land_surface_products,
        3: _space_products, 
        4: _space_weather_products,
        10: _oceanographic_products
    }

    _generating_processes = {
        0: 'Analysis',
        1: 'Initialization',
        2: 'Forecast',
        3: 'Bias Corrected Forecast',
        4: 'Ensemble Forecast',
        5: 'Probability Forecast',
        6: 'Forecast Error', 
        7: 'Analysis Error', 
        8: 'Observation',
        9: 'Climatological',
        10: 'Probability-Weighted Forecast',
        11: 'Bias-Corrected Ensemble Forecast',
        12: 'Post-processed Analysis',
        13: 'Post-processed Forecast',
        14: 'Nowcast',
        15: 'Hindcast',
        16: 'Physical Retrieval',
        17: 'Regression Analysis',
        18: 'Difference Between Two Forecasts',
        192: 'Forecast Confidence Indicator',
        193: 'Probability-matched Mean',
        194: 'Neighborhood Probability',
        195: 'Bias-Corrected and Downscaled Ensemble Forecast',
        196: 'Perturbed Analysis for Ensemble Initialization'
    }

    _time_unit_indicator = {
        0: 'Minute',
        1: 'Hour',
        2: 'Day',
        3: 'Month',
        4: 'Year',
        5: 'Decade',
        6: 'Normal',
        7: 'Century',
        10: '3 Hours',
        11: '6 Hours',
        12: '12 Hours'
    }

    # TODO
    _fixed_surface_types = {

    }

    # TODO
    _derived_forecast = {

    }

    _clustering_method = {
        0: 'Anomoly Correlation',
        1: 'Root Mean Square'
    }

class HorizontalAnalysisForecastTemplate(ProductTemplate):

    def __init__(self, data, discipline):
        super(HorizontalAnalysisForecastTemplate, self).__init__(self.product_type, 0, 'Analysis or forecast at a horizontal level or in a horizontal layer at a point in time', data)
        self._discipline_number = discipline
        self._product = self._products.get(self._discipline_number)

    @property
    def parameter_category_value(self):
        return _uint8.unpack_from(self._data, 9)[0]

    @property
    def parameter_category(self):
        return self._product.get(self.parameter_category_value)

    @property
    def parameter_number_value(self):
        return _uint8.unpack_from(self._data, 10)[0]

    @property
    def parameter_number(self):
        category = self.parameter_category
        if category is None:
            return None
        return category.parameters.get(self.parameter_number_value)

    @property
    def generating_process_value(self):
        return _uint8.unpack_from(self._data[11])[0]

    @property
    def generating_process(self):
        return self._generating_processes.get(self.generating_process_value)

    @property
    def hours_after_reference_time(self):
        return _uint16.unpack_from(self._data, 14)[0]

    @property
    def minutes_after_reference_time(self):
        return _uint8.unpack_from(self._data, 16)[0]

    @property
    def time_unit_value(self):
        return _uint8.unpack_from(self._data, 17)[0]

    @property
    def time_unit(self):
        return self._time_unit_indicator.get(self.time_unit_value)

    @property
    def forecast_time(self):
        return _uint32.unpack_from(self._data, 18)[0]

    @property
    def first_fixed_surface_value(self):
        return _uint8.unpack_from(self._data, 22)[0]

    @property
    def first_fixed_surface_scale_factor(self):
        return _uint8.unpack_from(self._data, 23)[0]

    @property
    def first_fixed_surface_scaled_value(self):
        return _uint32.unpack_from(self._data, 24)[0]

    @property
    def second_fixed_surface_value(self):
        return _uint8.unpack_from(self._data, 28)[0]

    @property
    def second_fixed_surface_scale_factor(self):
        return _uint8.unpack_from(self._data, 29)[0]

    @property
    def second_fixed_surface_scaled_value(self):
        return _uint32.unpack_from(self._data, 30)[0]

class DataRepresentationTemplate(BaseTemplate):

    _original_field_values = {
        0: 'Floating Point',
        1: 'Integer'
    }

    _matrix_coordinate_value_functions = {
        0: 'Explicit Coordinate Value Set',
        1: 'Linear Coordinates',
        11: 'Geometric Coordinates'
    }

    _matrix_coordinate_parameters = {
        1: 'Direction Degrees True',
        2: 'Frequency',
        3: 'Radial Number'
    }

    _group_splitting_methods = {
        0: 'Row by Row Splitting',
        1: 'General Group Splitting'
    }

    _missing_value_management = {
        0: 'No explicit missing values included with the data values',
        1: 'Primary missing values included within the data values',
        2: 'Primary and secondary missing values included within the data values'
    }

    _spatial_differencing_orders = {
        1: 'First-Order Spatial Differencing',
        2: 'Second-Order Spatial Differencing'
    }

    _floating_point_precisions = {
        1: 'IEEE 32-bit',
        2: 'IEEE 64-bit',
        3: 'IEEE 128-bit'
    }

    _compression_types = {
        0: 'Lossless',
        1: 'Lossy'
    }

class SimpleGridPointDataRepresentationTemplate(DataRepresentationTemplate):

    def __init__(self, data):
        super(SimpleGridPointDataRepresentationTemplate, self).__init__(self.data_rep_type, 0, 'Grid Point Data - Simple Packing', data)

    @property
    def reference_value(self):
        return _float32.unpack_from(self._data, 11)[0]

    @property
    def binary_scale_factor(self):
        return _uint16.unpack_from(self._data, 15)[0]

    @property
    def decimal_scale_factor(self):
        return _uint16.unpack_from(self._data, 17)[0]

    @property
    def bit_count(self):
        return _uint8.unpack_from(self._data, 19)[0]

    @property
    def original_field_value(self):
        return _uint8.unpack_from(self._data, 20)[0]

    @property
    def original_field_value_desc(self):
        return self._original_field_values.get(self.original_field_value)

class SimpleGridPointDataTemplate(BaseTemplate):

    def __init__(self, data):
        super(SimpleGridPointDataTemplate, self).__init__(self.data_type, 0, 'Grid Point Data - Simple Packing', data)

def find_template(template_type, number, data, discipline=-1):
    if template_type == BaseTemplate.grid_type:
        if number == 0:
            return LatitudeLongitudeGridTemplate(data)
    elif template_type == BaseTemplate.product_type:
        if number == 0:
            return HorizontalAnalysisForecastTemplate(data, discipline)
    elif template_type == BaseTemplate.data_rep_type:
        if number == 0:
            return SimpleGridPointDataRepresentationTemplate(data)
    elif template_type == BaseTemplate.data_type:
        if number == 0:
            return SimpleGridPointDataTemplate(data)
    return None

