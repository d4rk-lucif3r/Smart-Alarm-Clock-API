"""
This api  is a smart alarm clock intended to be run 24/7. It enables
the user to schedule alarms. The user is notified when
an alarm is up via text to speech and a notification
which is displayed in the notifications column. 
If the user has selected news and weather checkbox at the
time of setting an alarm then Each time alarm goes off
Latest news and weather update is played using text to speech
Covid news is played evrytime alarm goes off
"""
from covid_notifications import get_covid_data, clear_covid_news
from flask import Flask, request, render_template, redirect
from alarms import add_alarm, alarmTobeDeleted, get_alarms, clearAlarms
from news import get_news, clearNews
from notifications import update_notifications, notification_clear, clearAllNotification
from weather import get_weather, clearAllWeather
from logger import clearLogs,info_log

app = Flask(__name__)


@app.route('/')
def home():
    """
    This function is responsible for fetching a list of alarms, current
    weather, latest news and lates covid data. This data is
    fetched to be displayed on the main page.
    Whenever the html page refreshes news , weather and covid information
    is also fetched.
    """
    favicon = 'static\images\logo.ico'
    #False parameter is provide here so each time  news , weather
    #and covid info. is fetched it doesnt get played by text_to_speech
    get_news(False)
    get_weather(False)
    get_covid_data(False)
    title = "Smart Alarm Clock"
    alarm_list = get_alarms()
    notification_list = update_notifications()
    return render_template('home.html', alarm_list=alarm_list, notification_list=notification_list, favicon=favicon, title=title)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """
    This function is responsible for getting the details for an alarm
    stores alarm time , news and weather checkbox values in "title,isNews and is Weather"
    respectively and formats that into a dictionary and passes that into add_alarm function 
    alarms.py
    """
    title = request.args.get('alarm')
    if title:
        title = title.replace('T', '-')
        title = title+":00"

    label = request.args.get('two')
    isNews = request.args.get('news')
    if isNews == "news":
        isNews = "News Enabled"
    else:
        isNews = "News Not enabled"

    isWeather = request.args.get('weather')
    if isWeather == "weather":
        isWeather = "Weather Enabled"
    else:
        isWeather = "Weather Not enabled"
    if title:
        alarm = ({'title': title,
                  'label': label,
                  'news': isNews,
                  'weather': isWeather})
        add_alarm(alarm)
        return redirect('/')


@app.route('/delete_alarm', methods=['GET', 'POST'])
def delete_alarm():
    """
    Refer to delete alarm docstring in alarms.py
    """
    alarmTobeDeleted()
    return redirect('/')


@app.route('/notification-clear',
                  methods=['GET', 'POST'])
def notification_clear_function():
    """Refer to clear notification docstring in notifications.py"""
    notification_clear()
    return redirect('/')


@app.route('/clear',  methods=['GET', 'POST'])
def clearAll():
    """
    This function calls all clearing functions from all modules
    """
    clearAllNotification()
    clearAllWeather()
    clearNews()
    clearAlarms()
    clear_covid_news()
    clearLogs()
    info_log("Cleared all .json files")
    return redirect('/')


if __name__ == '__main__':
    smartClock.run(host='0.0.0.0',debug=True)
