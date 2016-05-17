from datetime import datetime, timedelta

from daysandunitslist import DaysAndUnitsList


def add_delta(duration, duration_unit):
    if duration_unit == 'minutes':
        return timedelta(minutes=duration)
    if duration_unit == 'hours':
        return timedelta(hours=duration)
    if duration_unit == 'days':
        return timedelta(days=duration)
    else:
        # Handle unexpected case
        return timedelta(minutes=0)


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


def validate_date(recv_start_date):
    """Use datetime.strptime() constructor validate the calendar"""
    try:
        datetime.strptime(recv_start_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_days(recv_days):
    """Decapitalise acronym and Eliminate duplication"""
    days_list = DaysAndUnitsList.days_list
    for i in range(len(recv_days)):
        recv_days[i] = recv_days[i].lower()
        if recv_days[i] not in days_list:
            return False
    recv_days = set(recv_days)
    return True


def validate_trigger_time(recv_trigger_time):
    """24 hours, 59 minutes"""
    try:
        datetime.strptime(recv_trigger_time, "%H:%M")
        return True
    except ValueError:
        return False


def validate_duration(duration):
    """No negative value"""
    try:
        duration = int(duration)
        if duration > 0:
            return True
        else:
            return False
    except ValueError as e:
        return False


def validate_duration_unit(recv_duration_unit):
    """Decapitalize and check in units_list"""
    units_list = DaysAndUnitsList.units_list
    recv_duration_unit = recv_duration_unit.lower()
    if recv_duration_unit in units_list:
        return True
    else:
        return False


def validate_trigger_identifiers(recv_trigger_identifiers):
    """Accept 2 identifiers per time"""
    if isinstance(recv_trigger_identifiers, list) is False:
        return False
    if len(recv_trigger_identifiers) > 2:
        return False
    return True


def is_non_json(input_json):
    checklist = ['start_date', 'days', 'trigger_time', 'duration', 'duration_unit', 'trigger_identifiers']
    errors = {
        "required_fields_missing": [],
        "invalid_inputs": []
    }
    for i in checklist:
        if input_json.get(i) is None:
            errors['required_fields_missing'].append(i + " is not found")
    return errors
