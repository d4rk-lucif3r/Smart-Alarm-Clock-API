"""
This module is responsible for fetching weather data from
Openweathermap using api key provided in config.json file
"""
import json
import time

import requests
import tempfile
from logger import error_log, info_log
from notifications import new_notification
from text_to_speech import tts
tmp_dir = tempfile.gettempdir()

def get_api_key() -> str:
    """
    This function fetches the openweathermap api key
    from the config file.
    """
    with open('assets/config.json', 'r') as config_file:
        api_keys = json.load(config_file)
    return api_keys['openweathermap']['api']


def get_weather(tts_enabled: bool) -> None:
    """
    This function fetches the weather data from openweathermap using
    api key provided in "config.json" and stores the data in 
    "weather.json" 
    New Notification and info log is created each time new data is fetched
    """
    # location
    location = 'New Delhi'
    api_key = get_api_key()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={} \
    &appid={}&units=metric'.format(location, api_key)
    new_weather = requests.get(url).json()
    with open(tmpdir+'/weather.json', 'w') as weather_file:
        json.dump(new_weather, weather_file, indent=2)
    weather_notification = ({'timestamp':
                             time.strftime('%H:%M:%S'),
                             'type': 'Weather',
                             'title': 'Current temperature in ' + new_weather['name']
                             + ' is '+str(new_weather['main']['temp'])
                             + "\n Minimum Temperature is " +
                             str(new_weather['main']['temp_min'])
                             + "\n and "
                             + "\n  Maximum Temperature is " +
                             str(new_weather['main']['temp_max']),
                             'description': ''})
    weather_log = ({'timestamp': time.strftime('%H:%M:%S'),
                    'type': 'weather',
                    'description': 'Current Weather in '
                    + new_weather['name']
                    + ' has been updated.',
                    'error': ''})
    new_notification(weather_notification)
    info_log(weather_log)
    if tts_enabled:
        try:
            tts('Current temperature in ' + new_weather['name']
                + 'is'+str(new_weather['main']['temp'])
                + "Minimum Temperature is" +
                str(new_weather['main']['temp_min'])
                + "and"
                + "Maximum Temperature is"+str(new_weather['main']['temp_max']))
        except RuntimeError :
            error_log(RuntimeError)
    with open(tmpdir+'/weather.json', 'w') as weather_file:
        json.dump(new_weather, weather_file, indent=2)


def clearAllWeather():
    """
    This function is responsible for clearing data in
    "weather.json" each time reset butoon on UI 
    is pressed
    """
    clearWeather = []
    with open(tmpdir+'/weather.json', 'w') as weather_file:
        json.dump(clearWeather, weather_file, indent=2)
