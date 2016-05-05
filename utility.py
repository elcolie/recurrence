import requests


def notify(job_id=None):
    r = requests.post('http://localhost:8000/api/scheduled-bod/', json={"job_id": job_id})


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