import argparse
import datetime
import grippy
import sys


def extract_metadata(messages):
    unique_vars = []
    dates = []
    array_var_count = 0

    for message in messages:
        model_time = message.sections[grippy.message.Message.IDENTIFICATION_SECTION_INDEX].reference_date
        hour = message.sections[grippy.message.Message.PRODUCT_DEFINITION_SECTION_INDEX].template.forecast_time
        date = model_time + datetime.timedelta(hours=hour)

        if not date in dates:
            dates.append(date)

        var = message.sections[grippy.message.Message.PRODUCT_DEFINITION_SECTION_INDEX].template.parameter_number.abbrev
        is_array_var = message.sections[grippy.message.Message.PRODUCT_DEFINITION_SECTION_INDEX].template.first_fixed_surface_type_value == 241
        var_index = message.sections[grippy.message.Message.PRODUCT_DEFINITION_SECTION_INDEX].template.first_fixed_surface_scaled_value

        if is_array_var:
            var += '_' + str(var_index)
            array_var_count += 1
            print(var)

        if not var in unique_vars:
            unique_vars.append(var)

    return {
        'vars': unique_vars,
        'dates': [d.isoformat() for d in dates],
        'array var count': array_var_count,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dump the metadata of a grib 2 file')
    parser.add_argument('filename', metavar='F', type=str, help='path to grib file to process')
    args = parser.parse_args()

    messages = grippy.message.read_messages(args.filename)
    if len(messages) == 0:
        print('Failed to extract grib2 data from ' + args.filename + ' . Make sure the file is valid and try again')
        sys.argv(1)

    metadata = extract_metadata(messages=messages)
    print('Grib Metadata for ' + args.filename + ':')
    print('------------------------------------------------')
    print('Array Variable Count: ' + str(metadata['array var count']))
    print('Variables (' + str(len(metadata['vars'])) + ') ' + ','.join(metadata['vars']))
    print('Dates: (' + str(len(metadata['dates'])) + ') ' + ','.join(metadata['dates']))
