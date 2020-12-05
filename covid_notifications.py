"""
This module is responsible for fetching and providing notifications for 
Covid Data. It fetches data from api.coronavirus.data.gov 
"""

import json
import time
from urllib.parse import urlencode

from requests import get
import requests

from logger import error_log, info_log
from notifications import new_notification
from text_to_speech import tts


def get_covid_data(tts_enabled: bool):
    """
    This function fetches data from api.coronavirus.data.gov using
    get method in requests module, creates a dictionary and store it 
    in "covid_notifications.json" file.
    New Notification and info log is created each time new data is found
    """
    url="https://api.covid19india.org/v4/data-2020-12-04.json"

    data=requests.get(url).json()
    new_covid_data = data['DL']

    with open('assets/covid_notifications.json', 'w') as covid_file:
        json.dump(new_covid_data, covid_file, indent=2)

        new_covid_notification = ({'timestamp':
                                   time.strftime('%H:%M:%S'),
                                   'type': 'Covid News',
                                   'title': "Covid News for Delhi" 
                                   + " with"
                                   + " Total confirmed cases " +
                                   str(new_covid_data['total']['confirmed'])
                                    + " Todays confirmed cases " +
                                   str(new_covid_data['delta']['confirmed'])})

        covid_logs = ({'timestamp': time.strftime('%H:%M:%S'),
                     'type': 'Covid News',
                     'description': "New Covid Data for Delhi",
                     'error': ''})
        new_notification(new_covid_notification)
        info_log(covid_logs)
        if tts_enabled:
            try:
                tts("Covid News for Delhi" 
                    + " with "
                    + " Total confirmed cases " +
                                   str(new_covid_data['total']['confirmed'])
                    + " Todays confirmed cases " +
                                   str(new_covid_data['delta']['confirmed']))
            except RuntimeError:
                error_log(RuntimeError)

    with open('assets/covid_notifications.json', 'w') as covid_file:
        json.dump(new_covid_data, covid_file, indent=2)

def clear_covid_news():
    """
    This function is responsible for clearing data in
    "covid_notifications.json" each time reset butoon on UI 
    is pressed
    """
    new_covid_data = []
    with open('assets/covid_notifications.json', 'w') as covid_file:
        json.dump(new_covid_data, covid_file, indent=2)
