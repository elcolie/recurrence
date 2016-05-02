from datetime import datetime, timedelta


def notify():
    temp_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp_str = "Notification alarms '{0}' ".format(temp_datetime)
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