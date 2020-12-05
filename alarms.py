"""
This Module is responsible for all the alarms and providing 
scheduled notifications
"""



import datetime
import json
import sched
import time
from threading import Thread

import schedule
from flask import request

from covid_notifications import get_covid_data
from logger import error_log, info_log, warning_log
from news import get_news
from notifications import new_notification
from text_to_speech import tts
from weather import get_weather


def add_alarm(alarm: dict) -> list:
    """
    This function reads all existing alarms from the alarms.json file, appends
    each one to a list, appends the new alarms to the same list and
    writes that list to the same json file. 
    """
    with open('assets/alarms.json', 'r') as alarms_file:
        # Attempts to load contents of the file. If it's empty, an
        # empty list is defined and a warning is sent to the log file.
        try:
            alarms_object = json.load(alarms_file)
        except Exception:
            alarms_object = []
            error_log(Exception)
    alarms_object.append(alarm.copy())
    with open('assets/alarms.json', 'w') as alarms_file:
        json.dump(alarms_object, alarms_file, indent=2)

    # Start alarm thread reset as the alarms json has changed.
    # return start_alarm()
    alarm_thread = Thread(target=start_alarm, args=(), daemon=True)
    alarm_thread.start()


def get_alarms() -> dict:
    """
    This function reads the alarms.json file and returns its contents to
    a dictionary.This dictionary is used to show alarms in UI
    """
    with open('assets/alarms.json', 'r') as alarms_file:
        try:
            alarm_list = json.load(alarms_file)
        except Exception:
            alarm_list = []
            error_log(Exception)
    return alarm_list


def alarmTobeDeleted():
    """
    This function allows the user to delete an alarm. The alarm time to
    be deleted is fetched using the request module into alarmToBeDelted variable.
    and it gets passed in delete_alarm function 
    """
    alarmToBeDeleted = request.args.get('alarm_item')

    if alarmToBeDeleted:
        alarmToBeDeleted = alarmToBeDeleted.replace('T', ' ')
    delete_alarm(alarmToBeDeleted)


def delete_alarm(alarmToBeDeleted):
    """
    This function takes an alarm argument which is to be deleted.
    Creates a new alarms object. The old alarms gets daved in "alarms_list"
    If no alarms are there then it will instantiate a new clean object "alarm_list"
    The for loop iterates through
    each alarm. If an alarm time is found that is not equal to the time
    the user has requested to delete, that alarm object is appended to
    a new list 'new_alarm_objects'.The edited list of alarms is then
    written to the json file and the start alarm thread is reset.
    """
    new_alarm_objects = []

    with open('assets/alarms.json', 'r') as alarms_file:
        try:
            alarm_list = json.load(alarms_file)
        except Exception:
            alarm_list = []
            error_log(Exception)

        for alarm in alarm_list:
            if alarm['title'] != alarmToBeDeleted:
                new_alarm_objects.append(alarm)

    with open('assets/alarms.json', 'w') as alarms_file:
        json.dump(new_alarm_objects, alarms_file, indent=2)
    info_log("deleted alarm"+alarmToBeDeleted)


def start_alarm() -> None:
    """
    This function is responsible for setting timers for each alarm.
    For each alarm, the difference in time between now and the time of
    the alarm  and adds each alarm to the
    schedular. This function runs on a separate thread each time the
    user loads the program.
    """
    alarm_schedule = sched.scheduler(time.time, time.sleep)
    time_when_alarm_is_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_when_alarm_is_created = datetime.datetime.strptime(
        time_when_alarm_is_created, "%Y-%m-%d %H:%M:%S")
    DAY = 86400
    news_call = False
    weather_call = False
    with open('assets/alarms.json', 'r') as alarms_file:
        try:
            alarm_list = json.load(alarms_file)
        except Exception:
            alarm_list = []
            warning_log(Exception)

    for alarm in alarm_list:
        # Alarm is a standard, one off alarm.
        # Date and time the alarm is set to go off.
        alarm_time = datetime.datetime.strptime(
            alarm['title'], '%Y-%m-%d-%H:%M:%S')
        # Time in seconds to when the alarm is due to go off.
        final_time = int(
            (alarm_time - time_when_alarm_is_created).total_seconds())
        if alarm['news'] == "News Enabled":
            news_call = True
        if alarm['weather'] == "Weather Enabled":
            weather_call = True

        # If the alarm is set at a time that is eariler than the
        # time of the alarm, add 24 hours to the time.
        if final_time < 0:
            final_time += DAY
        # Adds alarm to the scheduler.
        alarm_schedule.enter(final_time, 1, alarm_end,
                             (alarm_time, alarm, news_call, weather_call))

    alarm_schedule.run()
    schedule.run_pending()


def alarm_end(alarm_time: datetime.datetime, alarm: dict, news_call: bool, weather_call: bool) -> None:
    """
    This function runs when an alarm has gone off. The notification and log
    dictionaries are created including the necessary alarm data. 
    If the user has checked news and weather checkboxes then news and weather information
    will be played. Covid Data Nwews will be plaayed on every alarm
    """
    # Alarm Go off notification created
    alarm_notification = ({'timestamp': time.strftime('%H:%M:%S'),
                           'type': 'Alarm',
                           'title': ' Alarm scheduled for ' +
                                    str(alarm_time) +
                                    ' has gone off.',
                           'description': ''
                           })
    alarm_log = ({'timestamp': time.strftime('%H:%M:%S'),
                  'type': 'alarm',
                  'description': 'Alarm scheduled for ' +
                                 str(alarm_time) +
                                 ' has gone off.',
                  'error': ''
                  })
    new_notification(alarm_notification)
    info_log(alarm_log)
    tts("Alarm  "+str(alarm_time)+"has gone off")
    if news_call == True:
        get_news(True)
    if weather_call == True:
        get_weather(True)
    get_covid_data(True)


def clearAlarms():
    """
    This functions clears alarms.json file's content when reset button is clicked on 
    UI.
    """
    clearAllAlarms = []
    with open('assets/alarms.json', 'w') as alarms_file:
        json.dump(clearAllAlarms, alarms_file, indent=2)
