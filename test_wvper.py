import message
import helpers
import sys

mess = message.read_messages('multi_1.at_10m.t12z.f000.grib2')

for m in mess:
    if m.sections[3].template.parameter_number is not None:
        if m.sections[3].template.parameter_number.abbrev == 'WVPER':
            d = m

print(d.sections[3].template.parameter_number.abbrev)
print('----------------------------------------------')
print('ref: ' + str(d.sections[4].template.reference_value))
print('binscale: ' + str(d.sections[4].template.binary_scale_factor))
print('decimalscale: ' + str(d.sections[4].template.decimal_scale_factor))
print('bits: ' + str(d.sections[4].template.bit_count))
print('datapts: ' + str(d.sections[4].data_point_count))
print('firstpt: ' + str(helpers._uint8.unpack_from(d.sections[6]._data, 5)))
print('hasbmp: ' + str(d.sections[5].has_bitmap))
print('bitmappts: ' + str(d.sections[5].all_bit_truths))


#sys.stdout.buffer.write(d.sections[6]._data[6:6+d.sections[4].template.bit_count])