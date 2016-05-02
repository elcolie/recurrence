import os, sys
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, json, request
from utility import notify, return_data
from datetime import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/start', methods=['GET'])
def start_scheduler():
    """Get system up from crash or shutdown
    Usage: curl http://localhost:5000/recurrence/start
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


@app.route('/onetime/create', methods=['POST'])
def onetime_create():
    """
    Input : Name, YYYY-MM-DD HH:MM, Run immediate by not giving datetime
    Output : success, id, name
    Usages :
    Run when
    1. curl -H "Content-Type: application/json" -X POST -d '{"run_date":"2019-09-06 09:30", "name":"Switching circuit"}' http://localhost:5000/onetime/create
    2. curl -H "Content-Type: application/json" -X POST -d '{"run_date":"", "name":"Immediate Start"}' http://localhost:5000/onetime/create
    """
    recv_run_time = request.json['run_date']
    recv_name = request.json['name']
    if recv_run_time == "":
        try:
            instance = scheduler.add_job(notify, name=recv_name)
            data = return_data(True, instance)
            return str(data)
        except Exception as e:
            data = return_data(False,error_message=e)
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
    f = open('workfile.txt','w')    # Example how to visualize construction details
    scheduler.print_jobs(out=f)
    joblist = scheduler.get_jobs()
    new_list = []
    for i in joblist:
        data = {"id": i.id, "name": i.name}
        new_list.append(data)
    return str(new_list)


@app.route('/recurrence/create', methods=['POST'])
def create_job():
    """Create a job
    Input : name, day_of_week, start_time
    Output : success, id, name
    Usage : curl -H "Content-Type: application/json" -X POST -d '{"name":"Good Evening", "day_of_week":"sun", "start_time":"17:17"}' http://localhost:5000/recurrence/create
    """
    recv_day_of_week = request.json['day_of_week']
    recv_start_time = request.json['start_time']
    recv_start_hour, recv_start_minute = recv_start_time.split(':')
    recv_start_hour, recv_start_minute = int(recv_start_hour), int(recv_start_minute)
    recv_name = request.json['name']
    try:
        job_instance = scheduler.add_job(notify, 'cron', day_of_week=recv_day_of_week, hour=recv_start_hour, minute=recv_start_minute, name=recv_name)
        data = return_data(True, in_instance=job_instance)
        return data
    except Exception as e:
        data = return_data(False, error_message=e)
        return data


@app.route('/recurrence/edit', methods=['PUT'])
def edit_job():
    """Edit a job
    Input : id, name, day_of_week, start_time
    Output : id
    Usage : curl -H "Content-Type: application/json" -X PUT -d '{"id": "dc3d9acb052e47c9be310253937d644e","name":"Good Night", "day_of_week":"mon,sun,sat", "start_time":"18:18"}' http://localhost:5000/recurrence/edit
    """
    recv_id = request.json['id']
    recv_day_of_week = request.json['day_of_week']
    recv_start_time = request.json['start_time']
    recv_start_hour, recv_start_minute = recv_start_time.split(':')
    recv_start_hour, recv_start_minute = int(recv_start_hour), int(recv_start_minute)
    recv_name = request.json['name']
    try:
        # import pdb; pdb.set_trace()
        job_instance = scheduler.reschedule_job(recv_id, trigger='cron', day_of_week=recv_day_of_week, hour=recv_start_hour, minute=recv_start_minute)
        data = return_data(True, in_instance=job_instance)
        return data
    except Exception as e:
        data = return_data(False, error_message=e)
        return data


@app.route('/recurrence/delete', methods=['DELETE'])
def delete_job():
    """Create a job
    Input : id
    Output : Plain text
    Usage : curl -H "Content-Type: application/json" -X DELETE -d '{"id": "d345afd9d2ba4a3b924179fe87cdeda4"}' http://localhost:5000/recurrence/delete
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
    main()
