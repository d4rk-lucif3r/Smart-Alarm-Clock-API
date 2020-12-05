"""
This module is responsible for fetching and providing notifications for 
Covid Data. It fetches data from api.coronavirus.data.gov 
"""

import json
import time
from urllib.parse import urlencode

from requests import get

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
    ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
    AREA_TYPE = "nation"
    AREA_NAME = "england"

    filters = [
        f"areaType={ AREA_TYPE }",
        f"areaName={ AREA_NAME }"
    ]

    structure = {
        "date": "date",
        "name": "areaName",
        "code": "areaCode",
        "cases": {
            "daily": "newCasesByPublishDate",
            "cumulative": "cumCasesByPublishDate"
        },
        "deaths": {
            "daily": "newDeathsByDeathDate",
            "cumulative": "cumDeathsByDeathDate"
        }
    }

    api_params = {
        "filters": str.join(";", filters),
        "structure": json.dumps(structure, separators=(",", ":")),
        "latestBy": "newCasesByPublishDate"
    }

    encoded_params = urlencode(api_params)

    response = get(f"{ ENDPOINT }?{ encoded_params }", timeout=10)

    if response.status_code >= 400:
        error_log(f'Request failed: { response.text }')

    data = response.json()
    new_covid_data = data["data"]

    with open('covid_notifications.json', 'w') as covid_file:
        json.dump(new_covid_data, covid_file, indent=2)
        new_covid_notification = ({'timestamp':
                                   time.strftime('%H:%M:%S'),
                                   'type': 'Covid News',
                                   'title': "Covid News for " + str(new_covid_data[0]["name"])
                                   + " with"
                                   + " Total case count " +
                                   str(new_covid_data[0]
                                       ["cases"]["cumulative"])
                                   + " Daily Case count " +
                                   str(new_covid_data[0]["cases"]["daily"]),
                                   'description': ''})
        covid_logs = ({'timestamp': time.strftime('%H:%M:%S'),
                     'type': 'Covid News',
                     'description': "New Covid Data for"+str(new_covid_data[0]['name']),
                     'error': ''})
        new_notification(new_covid_notification)
        info_log(covid_logs)
        if tts_enabled:
            try:
                tts("Covid News for " + str(new_covid_data[0]["name"])
                    + " with "
                    + " Total case count " +
                    str(new_covid_data[0]["cases"]["cumulative"])
                    + " Daily Case count "+str(new_covid_data[0]["cases"]["daily"]))
            except RuntimeError:
                error_log(RuntimeError)

    with open('covid_notifications.json', 'w') as covid_file:
        json.dump(new_covid_data, covid_file, indent=2)



