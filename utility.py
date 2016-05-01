from datetime import datetime, timedelta


def change_bandwidth(description_message: str or None,
                        bandwidth: int or None):
    temp_str = "'{0}' : '{1}'".format(description_message, bandwidth)
    print(temp_str)


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
