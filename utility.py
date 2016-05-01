from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import Flask, json, request
app = Flask(__name__)
scheduler = BackgroundScheduler()


def change_bandwidth(bandwidth : int):
    print('Bandwidth Changed : %s' % bandwidth)


def example_cron():
    """
    http://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html#module-apscheduler.triggers.cron
    """
    print('Cron schedule has been scheduled')


def example_date():
    """
    http://apscheduler.readthedocs.io/en/latest/modules/triggers/date.html#module-apscheduler.triggers.date
    """
    alarm_time = datetime.now() + timedelta(seconds=10)
    print('One time date has been scheduled')


def example_interval():
    """
    http://apscheduler.readthedocs.io/en/latest/modules/triggers/interval.html#module-apscheduler.triggers.interval
    """
    scheduler.add_job(change_bandwidth, 'interval', seconds=3)
    print('Alarm! This alarm was scheduled')

