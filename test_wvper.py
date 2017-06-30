import message
import helpers
import sys

mess = message.read_messages('multi_1.at_10m.t12z.f000.grib2')
var = 'WVPER'

for m in mess:
    if m.sections[3].template.parameter_number is not None:
        if m.sections[3].template.parameter_number.abbrev == var:
            d = m

if d is None:
    print('Failed to find var: ' + var)
    sys.exit(0)

print(d.sections[3].template.parameter_number.abbrev)
print('----------------------------------------------')
print('ref: ' + str(d.sections[4].template.reference_value))
print('binscale: ' + str(d.sections[4].template.binary_scale_factor))
print('decimalscale: ' + str(d.sections[4].template.decimal_scale_factor))
print('bits: ' + str(d.sections[4].template.bit_count))
print('datapts: ' + str(d.sections[4].data_point_count))
print('datapts_ver: ' + str(d.sections[6].template.data_point_count))
print('firstpt: ' + str(helpers._uint8.unpack_from(d.sections[6]._data, 5)))
print('hasbmp: ' + str(d.sections[5].has_bitmap))
print('bitmappts: ' + str(d.sections[5].all_bit_truths))

print('time_unit_range: ' + str(d.sections[3].template.time_unit))
print('time: ' + str(d.sections[3].template.forecast_time))

print('start_lat: ' + str(d.sections[2].template.start_latitude))
print('lat_increment: ' + str(d.sections[2].template.i_direction_increment))
print('end_lat: ' + str(d.sections[2].template.end_latitude))
print('start_lon: ' + str(d.sections[2].template.start_longitude))
print('lon_increment: ' + str(d.sections[2].template.end_longitude))
print('end_lon: ' + str(d.sections[2].template.end_longitude))
print('num_points: ' + str(d.sections[2].data_point_count))
print('ni: ' + str(d.sections[2].template.parallel_point_count))
print('nj: ' + str(d.sections[2].template.meridian_point_count))
print('res_flags: '+ str(d.sections[2].template.resolution_component_flags))

print('scaled_values: ' + str(d.sections[6].scaled_values))



#sys.stdout.buffer.write(d.sections[6]._data[6:6+d.sections[4].template.bit_count])