import requests
import datetime
import multiprocessing
import message
import sys


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

if __name__ == '__main__':
    latest_model = latest_model_time()
    urls = [create_url(latest_model.hour, i, latest_model) for i in range(0, 183, 3)]

    pool = multiprocessing.Pool(processes=20)
    result = pool.map(fetch_grib_data, urls)
    if len(result) < 1:
        print('Failed to fetch grib data')
        sys.exit(0)
    grib_messages = [message.read_messages_raw(d) for d in result]
    print('Fetched ' + str(len(grib_messages)) + ' grib messages')