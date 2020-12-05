import json
from flask import request
from logger import error_log,warning_log


def new_notification(notification_object: dict) -> None:
    """
    Each time an alarm goes off, a change in weather has been detected
    or there's a new news story, the data is sent to this function. The
    data for that notification is then appended to the json file.
    """
    # Attempts to load contents of the file. If it's empty, an
    # empty list is defined and a warning is sent to the log file.
    with open('notifications.json', 'r') as notification_file:
        try:
            notifications = json.load(notification_file)
        except Exception as error:
            notifications = []
            warning_log(error)

    notifications.append(notification_object.copy())

    with open('notifications.json', 'w') as notification_file:
        json.dump(notifications, notification_file, indent=2)


def update_notifications() -> dict:
    """
    This function will run each time the page is refreshed.
    It returns the appropriate list of
    notifications depending if the 'Filter' button was pressed or the
    page was refreshed.
    """
    with open('notifications.json', 'r') as notification_file:
        try:
            notifications = json.load(notification_file)
        except Exception as error:
            notifications = []
            warning_log(error)
    return notifications


def notification_clear():
    notificationTobeDeleted = request.args.get('notif')
    new_notification_object = []

    with open('notifications.json', 'r') as notification_file:
        try:
            notification_list = json.load(notification_file)
        except Exception as error:
            notification_list = []
            error_log(error)

        for notification in notification_list:
            if notification['title'] != notificationTobeDeleted:
                new_notification_object.append(notification)

    with open('notifications.json', 'w') as notification_file:
        json.dump(new_notification_object, notification_file, indent=2)
        # Start the timer to run this function every 60 seconds.


