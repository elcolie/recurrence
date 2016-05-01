import os, sys

from flask import Flask, json, request
from utility import scheduler, change_bandwidth, example_cron, example_date, example_interval


app = Flask(__name__)

"""
    Sample Case : 8:00 down bandwidth to 5, then 18:00 up bandwidth to 10
    Sending :
    Receive JSON type : { "bandwidth" : 5 , "start_time"}
    curl -H "Content-Type: application/json" -X POST -d '{"schedule_type":"recurrence", "month" : ['Jan', 'Dec'], "start_time": "17:00""schedule_days": [1, 3, 5, 7]"stop_type" : "period","lifetime_quantity" : 1,"lifetime_unit" : "day","current_bandwidth" : 5,"new_bandwidth" : 10}' http://localhost:5000/recurrence/create
"""


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
    Usage: curl -H "Content-Type: application/json" -X POST -d '{"key":"value"}' http://localhost:5000/recurrence/create
    curl -H "Content-Type: application/json" -X POST -d '{"id":"C101", "seconds":3, "bandwidth":21}' http://localhost:5000/recurrence/create
    Input : JSON
    """
    if request.method == 'POST':
        recv_id = request.json['id'] # Choose wisly to be brief and concise meaning
        recv_seconds = request.json['seconds']
        recv_bandwidth = request.json['bandwidth']
        # import pdb; pdb.set_trace()

        scheduler.add_job(change_bandwidth, 'interval', seconds=recv_seconds, id=recv_id, args=[recv_bandwidth])
        return str(request.json)
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
    try:
        if sys.argv[1] == 'debug':
            app.debug = True
        app.run(host='localhost')
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler Stop")
        scheduler.shutdown()

if __name__ == '__main__':
    main()
