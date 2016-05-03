from datetime import datetime, timedelta


def notify(job_id=None):
    temp_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp_str = "Notification alarms '{0}' '{1}'".format(temp_datetime, job_id)
    print(temp_str)


def return_data(in_success, in_instance=None, error_message=None):
    if in_instance is None:
        data = {"success" : in_success,
                "id": None,
                "name": None}
    else:
        data = {"success": in_success,
                "id": in_instance.id,
                "name": in_instance.name,
                "error_msg": error_message}
    return str(data)