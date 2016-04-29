from datetime import datetime, timedelta
import os

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

"""
    Sample Case : 8:00 down bandwidth to 5, then 18:00 up bandwidth to 10
    Sending :
    Receive JSON type : { "bandwidth" : 5 , "start_time"}
"""

scheduler = BackgroundScheduler()

def change_bandwidth():
    print('Bandwidth Changed')

def up_bandwidth():
    print('Alarm! This alarm was scheduled')

def down_bandwidth():
    print("Hey, El! Get shit done!")


"""Create a job"""
@app.route('/recurrence/create')
def create_job():
    return "Job Created"

"""Get system up from crash or shutdown"""
@app.route('/recurrence')
def hello_world():
    scheduler.add_job(hello_el, 'interval', seconds=2)
    return 'Hello World!'

if __name__ == '__main__':
    url = 'sqlite:///hello.sqlite3'
    scheduler.add_jobstore('sqlalchemy', url=url)
    alarm_time = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(up_bandwidth, 'interval', seconds=3)
    print('To clear the alarms, delete the example.sqlite file.')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
        app.run(host='localhost')
    except (KeyboardInterrupt, SystemExit):
        print("You want to stop the progrm.")