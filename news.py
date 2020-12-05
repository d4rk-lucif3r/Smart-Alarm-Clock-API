"""
This module is responsible for fetching weather data from
newsapi using api key provided in config.json file
"""


import json
import time

import requests

from logger import error_log, info_log, warning_log
from notifications import new_notification
from text_to_speech import tts


def get_api_key() -> dict:
    """Fetches the newsapi api key from the config file."""
    with open('assets/config.json', 'r') as config_file:
        api_keys = json.load(config_file)
    return api_keys['newsapi']['api']


def get_news(tts_enbled: bool) -> None:
    """
    This function fetches the weather data from newssapi using
    api key provided in "config.json" and stores the data in 
    "news.json" 
    New Notification and info log is created each time new data is fetched
    """
    api_key = get_api_key()
    country = 'gb'
    url = 'https://newsapi.org/v2/top-headlines?country={}&apiKey={}' \
        .format(country, api_key)
    new_news = requests.get(url).json()
    with open('assets/news.json', 'w') as news_file:
        json.dump(new_news, news_file, indent=2)

    for i in range(3):
        news_notification = ({'timestamp':
                              time.strftime('%H:%M:%S'),
                              'type': 'News',
                              'title': new_news
                              ['articles'][i]['title'],
                              'description': ''})
        news_log = ({'timestamp': time.strftime('%H:%M:%S'),
                     'type': 'news',
                     'description': 'New news articles'
                     + new_news['articles'][i]['title'],
                     'error': ''})
        new_notification(news_notification)
        info_log(news_log)
        if(tts_enbled):
            try:
                tts('New news story.'
                    + new_news['articles'][i]['title'])
            except RuntimeError:
                error_log(RuntimeError)

    with open('assets/news.json', 'w') as news_file:
        json.dump(new_news, news_file, indent=2)


def clearNews():
    """
    This function is responsible for clearing data in
    "news.json" each time reset butoon on UI 
    is pressed
    """
    clearAllNews = []
    with open('assets/news.json', 'w') as news_file:
        json.dump(clearAllNews, news_file, indent=2)
