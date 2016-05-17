import os
import sys
import requests

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from flask_restful import Resource, Api

from utility import return_data, add_delta, validate_date, validate_days, validate_trigger_time, \
    validate_duration, validate_duration_unit, validate_trigger_identifiers, is_non_json
from dateutil.relativedelta import *
from daysandunitslist import DaysAndUnitsList
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)
scheduler = BackgroundScheduler()


@app.route('/recurrence', methods=['GET'])
def list_job():
    """List all jobs
    Input : No input
    Output : string of list contains dictionary id as a key and name as a value
    Usage : curl http://localhost:5000/recurrence
    """
    f = open('workfile.txt', 'w')  # Example how to visualize construction details
    scheduler.print_jobs(out=f)
    joblist = scheduler.get_jobs()
    new_list = []
    for i in joblist:
        data = {"id": i.id, "name": i.name}
        new_list.append(data)
    return str(new_list)


def single_notify(recv_trigger_identifiers):
    """Sudden run"""
    r = requests.post('http://localhost:8000/api/scheduled-bod/', json={"job_id": recv_trigger_identifiers})


def notify(recv_trigger_identifiers, duration=None, duration_unit=None):
    r = requests.post('http://localhost:8000/api/scheduled-bod/', json={"job_id": recv_trigger_identifiers[0]})
    next_run_time = datetime.now() + add_delta(duration, duration_unit)
    second_job = scheduler.add_job(single_notify,
                                   'date',
                                   id=recv_trigger_identifiers[1],
                                   run_date=next_run_time,
                                   args=[recv_trigger_identifiers[1]])


class RecurrenceDays(Resource):
    start_date = None
    days = None
    trigger_time = None
    duration = None
    duration_unit = None
    trigger_identifiers = None
    errors = None
    json = None

    def get_start_hours_and_minutes(self):
        my_hour = datetime.strptime(self.trigger_time, '%H:%M')
        hour, minute = my_hour.hour, my_hour.minute
        return hour, minute

    def add_job_days(self):
        days_of_week = ",".join(self.days)
        start_hour, start_minute = self.get_start_hours_and_minutes()

        first_job = scheduler.add_job(notify,
                                      'cron',
                                      id=self.trigger_identifiers[0],
                                      day_of_week=days_of_week,
                                      hour=start_hour,
                                      minute=start_minute,
                                      start_date=self.start_date,
                                      args=[self.trigger_identifiers])

    def post(self):
        self.json = request.json
        self.errors = is_non_json(self.json)
        if len(self.errors['required_fields_missing']) > 0:
            return self.errors, 400

        # All field are present. Then validate the inputs. And return error detail with example.
        if validate_date(self.json.get('start_date')) is False:
            self.errors["invalid_inputs"].append("start_date is invalid format. Ex: 2009-09-29")
        if validate_days(self.json.get('days')) is False:
            self.errors["invalid_inputs"].append("days is invalid format. Ex: ['fri', 'wed']")
        if validate_trigger_time(self.json.get('trigger_time')) is False:
            self.errors["invalid_inputs"].append("trigger_time is invalid format. (24-hour format) Ex: 05:05")
        if validate_duration(self.json.get('duration')) is False:
            self.errors["invalid_inputs"].append("duration must be positive value")
        if validate_duration_unit(self.json.get('duration_unit')) is False:
            self.errors["invalid_inputs"].append("duration_unit are one of " + str(DaysAndUnitsList.units_list))
        if validate_trigger_identifiers(self.json.get('trigger_identifiers')) is False:
            self.errors["invalid_inputs"].append("trigger_identifiers must not has more than 2")

        if len(self.errors["invalid_inputs"]) > 0:
            return self.errors, 400
        else:
            start_date = self.json.get('start_date')
            days = self.json.get('days')
            trigger_time = self.json.get('trigger_time')
            duration = self.json.get('duration')
            duration_unit = self.json.get('duration_unit')
            trigger_identifiers = self.json.get('trigger_identifiers')
            self.add_job_days()
            return {}, 200


@app.route('/recurrence/days', methods=['DELETE'])
def delete_job():
    """Create a job
    Input : id
    Output : Plain text
    Usage : curl -H "Content-Type: application/json" -X DELETE -d '{"id": "d345afd9d2ba4a3b924179fe87cdeda4"}' http://localhost:5000/recurrence/days
    """
    recv_id = request.json['id']
    try:
        scheduler.remove_job(recv_id)
        data = return_data(True)
        return data
    except Exception as e:
        data = return_data(False)
        return data


def main(*args, **kwargs):
    url = 'sqlite:///hello.sqlite3'
    scheduler.add_jobstore('sqlalchemy', url=url)
    print('To clear the alarms, delete the hello.sqlite3 file.')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    scheduler.start()
    try:
        if len(sys.argv) > 2 and sys.argv[1] == 'debug':
            app.debug = True
        else:
            app.debug = False
        app.run(host='localhost')
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler Stop")
        scheduler.shutdown()


if __name__ == '__main__':
    api.add_resource(RecurrenceDays, '/recurrence/days')
    main()
