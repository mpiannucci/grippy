import requests
import datetime
import multiprocessing
import message
import sys
import helpers


base_url = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_wave_multi.pl?file=multi_1.at_10m.t{}z.f{}.grib2&all_lev=on&all_var=on&subregion=&leftlon=-71&rightlon=-70&toplat=41&bottomlat=40&dir=%2Fmulti_1.{}'


def create_url(model_run, hour, model_date):
    model_run_str = str(model_run).rjust(2, '0')
    hour_str = str(hour).rjust(3, '0')
    date_str = model_date.strftime('%Y%m%d')
    return base_url.format(model_run_str, hour_str, date_str)

def latest_model_time():
    current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=-5)
    latest_model_hour = current_time.hour - (current_time.hour % 6)
    current_time = current_time + datetime.timedelta(hours=-(current_time.hour-latest_model_hour))
    current_time = datetime.datetime(current_time.year, current_time.month, current_time.day, current_time.hour, 0)
    return current_time

def fetch_grib_data(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return []
    return resp.content

def read_var_info(timestep_messages, var):
    for m in timestep_messages:
        if m.section_count < 3:
            continue
        if m.sections[3].template.parameter_number is not None:
            if m.sections[3].template.parameter_number.abbrev == var:
                d = m

    if d is None:
        print('Failed to find var: ' + var)
        return False

    print(d.sections[3].template.parameter_number.abbrev)
    print('----------------------------------------------')
    print('ref: ' + str(d.sections[4].template.reference_value))
    print('binscale: ' + str(d.sections[4].template.binary_scale_factor))
    print('decimalscale: ' + str(d.sections[4].template.decimal_scale_factor))
    print('bits: ' + str(d.sections[4].template.bit_count))
    print('datapts: ' + str(d.sections[4].data_point_count))
    print('datapts_ver: ' + str(d.sections[6].template.data_point_count))
    #print('firstpt: ' + str(helpers._uint8.unpack_from(d.sections[6]._data, 5)))
    print('hasbmp: ' + str(d.sections[5].has_bitmap))
    print('bitmappts: ' + str(d.sections[5].all_bit_truths))
    print('emptyval: ' + str())
    
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

    print('scaled_values: ' + str(d.sections[6].all_scaled_values(d.sections[5].all_bit_truths)))

if __name__ == '__main__':
    latest_model = latest_model_time()
    urls = [create_url(latest_model.hour, i, latest_model) for i in range(0, 183, 3)]
    print(urls[0])

    pool = multiprocessing.Pool(processes=20)
    result = pool.map(fetch_grib_data, urls)
    if len(result) < 1:
        print('Failed to fetch grib data')
        sys.exit(0)
    grib_messages = [message.read_messages_raw(d) for d in result]
    print('Fetched ' + str(len(grib_messages)) + ' grib messages')
    print('--------------------------------------------------------')
    print('Variables Found: Timesteps')
    for grib_timestep in grib_messages:
        read_var_info(grib_timestep, 'WVPER')

        vars = []
        for grib in grib_timestep:
            if grib.sections[3].template.parameter_number is None:
                continue
            vars.append(grib.sections[3].template.parameter_number.abbrev)
        print('Timestep: ' + str(grib_timestep[0].sections[3].template.forecast_time))
        print(vars)