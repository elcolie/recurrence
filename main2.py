# sqlalchemy.py 
from sqlalchemy import *
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
from apscheduler.scheduler import Scheduler
from datetime import datetime, timedelta
import time

def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)

# APScheduler Configure Options
_g_aps_default_config = {
    'apscheduler.standalone' : True,
    'apscheduler.jobstore.default.class' : 'apscheduler.jobstores.sqlalchemy_store:SQLAlchemyJobStore',
    'apscheduler.jobstore.default.url' : 'postgresql://el@localhost/apschedulerdb',
    'apscheduler.jobstore.default.tablename' : 'mytable'
}

if __name__ == '__main__':

    scheduler = Scheduler(_g_aps_default_config)

    alarm_time = datetime.now() + timedelta(seconds=10)
    scheduler.add_date_job(alarm, alarm_time, name='alarm1', args=[datetime.now()])
    print('alarms added: %s' % alarm_time)

    alarm_time = datetime.now() + timedelta(seconds=15)
    scheduler.add_date_job(alarm, alarm_time, name='alarm2', args=[datetime.now()])
    print('alarms added: %s' % alarm_time)

    alarm_time = datetime.now() + timedelta(seconds=20)
    scheduler.add_date_job(alarm, alarm_time, name='alarm3', args=[datetime.now()])
    print('alarms added: %s' % alarm_time)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        pass