import os, sys
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta, datetime
from flask import Flask, json, request


app = Flask(__name__)
scheduler = BackgroundScheduler()

"""
    Sample Case : 8:00 down bandwidth to 5, then 18:00 up bandwidth to 10
    Sending :
    Receive JSON type : { "bandwidth" : 5 , "start_time"}
    curl -H "Content-Type: application/json" -X POST -d '{"schedule_type":"recurrence", "month" : ['Jan', 'Dec'], "start_time": "17:00""schedule_days": [1, 3, 5, 7]"stop_type" : "period","lifetime_quantity" : 1,"lifetime_unit" : "day","current_bandwidth" : 5,"new_bandwidth" : 10}' http://localhost:5000/recurrence/create
"""


def change_bandwidth(description_message: str or None,
                     bandwidth: int or None):
    temp_str = "'{0}' : '{1}'".format(description_message, bandwidth)
    print(temp_str)


@app.route('/recurrence/start', methods=['GET'])
def start_scheduler():
    """Get system up from crash or shutdown
    Usage: curl http://localhost:5000/recurrence/start
    """
    scheduler.start()
    return 'Scheduler Started\n'


@app.route('/recurrence/shutdown', methods=['GET'])
def stop_scheduler():
    """
    Shutdown will not be able to start again by REST APIs
    """
    scheduler.shutdown()
    return 'Scheduler Shutdown\n'


@app.route('/recurrence/', methods=['GET'])
def list_job():
    """List all jobs
    Usage : curl http://locahost:5000/recurrence
    """
    list_jobs = scheduler.print_jobs()
    temp_str = str(list_jobs) + '\n' # Wonder why it has None return
    return temp_str


@app.route('/recurrence/create', methods=['POST'])
def create_job():
    """Create a job
    First Receiving the JSON order.
    Second Decompose in to 2 jobs.
        1. Start changing bandwidth and
        2. Start undoing bandwidth
    Usage:
    curl -H "Content-Type: application/json" -X POST -d '{"schedule_type":"recurrecen","day_of_week":"mon,wed,fri","start_time":"06:00","bandwidth1": 10,"end_time":"18:00","bandwidth2":20}' http://localhost:5000/recurrence/create
    Input : JSON
    Apscheduler will create 2 josb base on given id
    """
    if request.method == 'POST':
        recv_schedule_type = request.json['schedule_type']
        recv_day_of_week = request.json['day_of_week']

        recv_start_time = request.json['start_time']
        recv_hour1, recv_minute1 = recv_start_time.split(':')
        recv_hour1, recv_minute1 = int(recv_hour1), int(recv_minute1)
        recv_bandwidth1 = request.json['bandwidth1']

        recv_end_time = request.json['end_time']
        recv_hour2, recv_minute2 = recv_end_time.split(':')
        recv_hour2, recv_minute2 = int(recv_hour2), int(recv_minute2)
        recv_bandwidth2 = request.json['bandwidth2']

        recv_id1 = "'{0}'-'{1}'-'start : '{2}'-'{3}' Mbps".format(recv_schedule_type, recv_day_of_week, recv_start_time, recv_bandwidth1)
        recv_id2 = "'{0}'-'{1}'-'start : {2}'-'{3}' Mbps".format(recv_schedule_type, recv_day_of_week, recv_end_time, recv_bandwidth2)

        try:
            # First change
            scheduler.add_job(change_bandwidth, 'cron', day_of_week=recv_day_of_week,
                              hour=recv_hour1, minute=recv_minute1, id=recv_id1, args=['Simple Message', recv_bandwidth1])

            # Second change
            scheduler.add_job(change_bandwidth, 'cron', day_of_week=recv_day_of_week,
                              hour=recv_hour2, minute=recv_minute2, id=recv_id2, args=['Simple Message', recv_bandwidth2])
            return "Add job Success\n"
        except Exception as e:
            return e
    else:
        return '404'


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


def main(*args, **kwargs):
    url = 'sqlite:///hello.sqlite3'
    scheduler.add_jobstore('sqlalchemy', url=url)
    print('To clear the alarms, delete the hello.sqlite3 file.')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    scheduler.start()
    try:
        if sys.argv[1] == 'debug':
            app.debug = True
        app.run(host='localhost')
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler Stop")
        scheduler.shutdown()

if __name__ == '__main__':
    main()
