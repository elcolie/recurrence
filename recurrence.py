import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from flask_restful import Resource, Api

from utility import notify, return_data
from dateutil.relativedelta import *
from daysandunitslist import DaysAndUnitsList
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)
scheduler = BackgroundScheduler()


@app.route('/start', methods=['GET'])
def start_scheduler():
    """Get system up from crash or shutdown
    Usage: curl http://localhost:5000/start
    """
    scheduler.start()
    return 'Scheduler Started\n'


@app.route('/shutdown', methods=['GET'])
def stop_scheduler():
    """
    Shutdown will not be able to start again by REST APIs
    """
    scheduler.shutdown()
    return 'Scheduler Shutdown\n'


@app.route('/onetime', methods=['POST'])
def onetime_create():
    """
    Input : Name, YYYY-MM-DD HH:MM, Run immediate by not giving datetime
    Output : success, id, name
    Usages :
    Run when
    1. curl -H "Content-Type: application/json" -X POST -d '{"run_date":"2019-09-06 09:30", "name":"Switching circuit"}' http://localhost:5000/onetime
    2. curl -H "Content-Type: application/json" -X POST -d '{"run_date":"", "name":"Immediate Start"}' http://localhost:5000/onetime
    """
    recv_run_time = request.json['run_date']
    recv_name = request.json['name']
    if recv_run_time == "":
        try:
            instance = scheduler.add_job(notify, name=recv_name)
            data = return_data(True, instance)
            return str(data)
        except Exception as e:
            data = return_data(False, error_message=e)
        finally:
            return data
    else:
        recv_run_time = datetime.strptime(recv_run_time, '%Y-%m-%d %H:%M')
        try:
            instance = scheduler.add_job(notify, run_date=recv_run_time, name=recv_name)
            data = return_data(True, instance)
        except Exception as e:
            data = return_data(False, error_message=e)
        finally:
            return data


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


class Recurrence(Resource):
    json = None
    recv_start_date = None
    recv_end_date = None
    recv_days = None
    recv_trigger_time = None
    recv_duration = None
    recv_duration_unit = None
    recv_trigger_identifiers = None
    errors = None

    def validate_date(self, recv_start_date):
        """Use datetime.strptime() constructor validate the calendar"""
        try:
            datetime.strptime(recv_start_date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_days(self, recv_days):
        """Decapitalise acronym and Eliminate duplication"""
        days_list = DaysAndUnitsList.days_list
        for i in range(len(recv_days)):
            recv_days[i] = recv_days[i].lower()
            if recv_days[i] not in days_list:
                return False
        self.recv_days = set(recv_days)
        return True

    def validate_trigger_time(self, recv_trigger_time):
        """24 hours, 59 minutes"""
        try:
            datetime.strptime(recv_trigger_time, "%H:%M")
            return True
        except ValueError:
            return False

    def validate_duration(self, recv_duration):
        """No negative value"""
        self.recv_duration = int(recv_duration)
        if recv_duration > 0:
            return True
        else:
            return False

    def validate_duration_unit(self, recv_duration_unit):
        """Decapitalize and check in units_list"""
        units_list = DaysAndUnitsList.units_list
        recv_duration_unit = recv_duration_unit.lower()
        if recv_duration_unit in units_list:
            return True
        else:
            return False

    def validate_trigger_identifiers(self, recv_trigger_identifiers):
        """Accept 2 identifiers per time"""
        if isinstance(recv_trigger_identifiers, list) is False:
            return False
        if len(recv_trigger_identifiers) > 2:
            return False
        return True

    def get_start_hours_and_minutes(self):
        my_hour = datetime.strptime(self.recv_trigger_time, '%H:%M')
        hour, minute = my_hour.hour, my_hour.minute
        return hour, minute

    def get_end_hours_and_minutes(self, duration, duration_unit):
        """delta_time is intentionally to use with duration"""
        if duration_unit == 'minutes':
            return relativedelta(minutes=duration)
        elif duration_unit == 'hours':
            return relativedelta(hours=duration)
        elif duration_unit == 'days':
            return relativedelta(days=duration)

    def add_second_job(self):
        end_datetimes_list = []
        # Find reference monday in code. Easier when maintained.
        start_datetime_str = " ".join([self.recv_start_date, self.recv_trigger_time])
        today = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")

        ref_monday = today + timedelta(days=-today.weekday(), weeks=1)
        ref_tueday = ref_monday + timedelta(days=1)
        ref_wedday = ref_tueday + timedelta(days=1)
        ref_thuday = ref_wedday + timedelta(days=1)
        ref_friday = ref_thuday + timedelta(days=1)
        ref_satday = ref_friday + timedelta(days=1)
        ref_sunday = ref_satday + timedelta(days=1)

        for i in self.recv_days:
            if i == "mon":
                nexttime = ref_monday + self.get_end_hours_and_minutes(self.recv_duration, self.recv_duration_unit)
                end_datetimes_list.append(nexttime)
            if i == "tue":
                nexttime = ref_tueday + self.get_end_hours_and_minutes(self.recv_duration, self.recv_duration_unit)
                end_datetimes_list.append(nexttime)
            if i == "wed":
                nexttime = ref_wedday + self.get_end_hours_and_minutes(self.recv_duration, self.recv_duration_unit)
                end_datetimes_list.append(nexttime)
            if i == "thu":
                nexttime = ref_thuday + self.get_end_hours_and_minutes(self.recv_duration, self.recv_duration_unit)
                end_datetimes_list.append(nexttime)
            if i == "fri":
                nexttime = ref_friday + self.get_end_hours_and_minutes(self.recv_duration, self.recv_duration_unit)
                end_datetimes_list.append(nexttime)
            if i == "sat":
                nexttime = ref_satday + self.get_end_hours_and_minutes(self.recv_duration, self.recv_duration_unit)
                end_datetimes_list.append(nexttime)
            if i == "sun":
                nexttime = ref_sunday + self.get_end_hours_and_minutes(self.recv_duration, self.recv_duration_unit)
                end_datetimes_list.append(nexttime)
        days_of_week_str = ""
        for day in end_datetimes_list:
            days_of_week_str += str(day.weekday()) + ','
        days_of_week_str = days_of_week_str[:len(days_of_week_str) - 1]  # Delete last comma
        end_hour, end_minute = end_datetimes_list[0].hour, end_datetimes_list[0].minute
        second_job = scheduler.add_job(notify,
                                       'cron',
                                       id=self.recv_trigger_identifiers[1],
                                       day_of_week=days_of_week_str,
                                       hour=end_hour,
                                       minute=end_minute,
                                       start_date=self.recv_start_date,
                                       end_date=self.recv_end_date,
                                       args=[self.recv_trigger_identifiers[1]])

    def addjob(self):
        temp_str = ""
        for i in self.recv_days:  # set(['mon', 'tue'])
            temp_str += i + ','
        days_of_week = temp_str[:len(temp_str) - 1]  # "mon,tue"
        start_hour, start_minute = self.get_start_hours_and_minutes()
        first_job = scheduler.add_job(notify,
                                      'cron',
                                      id=self.recv_trigger_identifiers[0],
                                      day_of_week=days_of_week,
                                      hour=start_hour,
                                      minute=start_minute,
                                      start_date=self.recv_start_date,
                                      end_date=self.recv_end_date,
                                      args=[self.recv_trigger_identifiers[0]])
        # second job
        self.add_second_job()

    def post(self):
        self.json = request.json
        self.recv_start_date = self.json.get('start_date')
        self.recv_end_date = self.json.get('end_date')
        self.recv_days = self.json.get('days')
        self.recv_trigger_time = self.json.get('trigger_time')
        self.recv_duration = self.json.get('duration')
        self.recv_duration_unit = self.json.get('duration_unit')
        self.recv_trigger_identifiers = self.json.get('trigger_identifiers')
        self.recv_job_name = self.json.get('job_name')
        self.errors = {
            "required_fields_missing": [],
            "invalid_inputs": []
        }
        # Check fields are given.
        # recv_end_date not given it is None by default. Not cause an error.
        if self.recv_start_date is None:
            self.errors["required_fields_missing"].append("start_date")
        if self.recv_days is None:
            self.errors["required_fields_missing"].append("days")
        if self.recv_trigger_time is None:
            self.errors["required_fields_missing"].append("trigger_time")
        if self.recv_duration is None:
            self.errors["required_fields_missing"].append("duration")
        if self.recv_duration_unit is None:
            self.errors["required_fields_missing"].append("duration_unit")
        if self.recv_trigger_identifiers is None:
            self.errors["required_fields_missing"].append("trigger_identifiers")
        if len(self.errors["required_fields_missing"]) > 0:
            return self.errors, 400
        else:
            # All field are present. Then validate the inputs.
            if self.validate_date(self.recv_start_date) is False:
                self.errors["invalid_inputs"].append("start_date is invalid format")
            if self.validate_days(self.recv_days) is False:
                self.errors["invalid_inputs"].append("days is invalid format")
            if self.validate_trigger_time(self.recv_trigger_time) is False:
                self.errors["invalid_inputs"].append("trigger_time is invalid format")
            if self.validate_duration(self.recv_duration) is False:
                self.errors["invalid_inputs"].append("duration must not be a negative value")
            if self.validate_duration_unit(self.recv_duration_unit) is False:
                self.errors["invalid_inputs"].append("duration_unit are one of " + str(DaysAndUnitsList.units_list))
            if self.validate_trigger_identifiers(self.recv_trigger_identifiers) is False:
                self.errors["invalid_inputs"].append("trigger_identifiers must not has more than 2")
            if len(self.errors["invalid_inputs"]) > 0:
                return self.errors, 400
            else:
                self.addjob()
                return {}, 200


@app.route('/recurrence', methods=['PUT'])
def edit_job():
    """Edit a job
    Input : id, name, day_of_week, start_time
    Output : id
    Usage : curl -H "Content-Type: application/json" -X PUT -d '{"id": "dc3d9acb052e47c9be310253937d644e","name":"Good Night", "day_of_week":"mon,sun,sat", "start_time":"18:18"}' http://localhost:5000/recurrence
    """
    recv_id = request.json['id']
    recv_day_of_week = request.json['day_of_week']
    recv_start_time = request.json['start_time']
    recv_start_hour, recv_start_minute = recv_start_time.split(':')
    recv_start_hour, recv_start_minute = int(recv_start_hour), int(recv_start_minute)
    recv_name = request.json['name']
    try:
        # import pdb; pdb.set_trace()
        job_instance = scheduler.reschedule_job(recv_id, trigger='cron', day_of_week=recv_day_of_week,
                                                hour=recv_start_hour, minute=recv_start_minute)
        data = return_data(True, in_instance=job_instance)
        return data
    except Exception as e:
        data = return_data(False, error_message=e)
        return data


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
    api.add_resource(Recurrence, '/recurrence/days')
    main()
