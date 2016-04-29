from datetime import datetime, timedelta
import os

from flask import Flask, json, request
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

"""
    Sample Case : 8:00 down bandwidth to 5, then 18:00 up bandwidth to 10
    Sending :
    Receive JSON type : { "bandwidth" : 5 , "start_time"}
    curl -H "Content-Type: application/json" -X POST -d '{"schedule_type":"recurrence", "month" : ['Jan', 'Dec'], "start_time": "17:00""schedule_days": [1, 3, 5, 7]"stop_type" : "period","lifetime_quantity" : 1,"lifetime_unit" : "day","current_bandwidth" : 5,"new_bandwidth" : 10}' http://localhost:5000/recurrence/create
"""

scheduler = BackgroundScheduler()


def change_bandwidth():
    print('Bandwidth Changed')


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


@app.route('/recurrence/start', methods=['GET'])
def hello_world():
    """Get system up from crash or shutdown
    Usage: curl http://localhost:5000/recurrence
    """
    scheduler.start()
    return 'Hello, Scheduler Started\n'  # It is an ordinary response! LoL


@app.route('/recurrence/', methods=['GET'])
def list_job():
    """List all jobs
    Usage : curl http://locahost:5000/recurrence
    """
    return "List all jobs\n"


@app.route('/recurrence/create', methods=['POST'])
def create_job():
    """Create a job
    Usage: curl -H "Content-Type: application/json" -X POST -d '{"key":"value"}' http://localhost:5000/recurrence/create
    Input : JSON
    """
    # data = request.json
    if request.method == 'POST':
        return request.json
    else:
        return '404'
    return "Job Created"


@app.route('/recurrence/edit', methods=['PUT'])
def edit_job():
    """Edit a job
    Usage: curl http://localhost:5000/recurrence/edit
    Input : JSON
    """
    return "Job Edited"


@app.route('/recurrence/delete', methods=['DELETE'])
def delete_job():
    """Create a job
    Usage: curl http://localhost:5000/recurrence/delete
    Input : JSON
    """
    return "Job Deleted"


def main():
    url = 'sqlite:///hello.sqlite3'
    scheduler.add_jobstore('sqlalchemy', url=url)
    print('To clear the alarms, delete the hello.sqlite3 file.')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        app.run(host='localhost')
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler Stop")
        scheduler.stop()

if __name__ == '__main__':
    main()
