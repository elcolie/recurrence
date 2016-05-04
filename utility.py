from datetime import datetime, timedelta
import requests

url = 'localhost:8099/scheduled-bod'
def notify(job_id=None):
    r = requests.post('http://localhost:9000/scheduled-bod', json={'job_id': 'Give me strength'})
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