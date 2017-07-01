import requests
import datetime


base_url = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_wave_multi.pl?file=multi_1.at_10m.t{}z.f{}.grib2&all_lev=on&all_var=on&subregion=&leftlon=-71&rightlon=-70&toplat=41&bottomlat=40&dir=%2Fmulti_1.{}'

def create_url(model_run, hour, date):
    model_run_str = str(model_run).rjust(2, '0')
    hour_str = str(hour).rjust(3, '0')
    date_str = date.strftime()
