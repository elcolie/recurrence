# recurrence
RESTful backend APIs UIH portal

## Recommend Python version
3.5.1

## Dependencies:
As noted in `requirement.txt`

## Installation :
pip install pip-tools
pip-compile requirement.in
It will generate `requirement.txt` then
pip install -r requirement.txt


## Normal run on localhost port 5000:
python recurrence.py

## Debugging mode on localhost port 5000:
python recurrence.py debug

## CRUD
**Create :**
Schedule a trigger (REST API)
HTTP: POST
URL: '/recurrence/days'
Input:
+ start_date: string             // format: %Y-%m-%d (24-hour format). Ex: 2009-09-09
- end_date: string               // format: %Y-%m-%d (24-hour format). Program is terminated on this day.
+ days: [enum]                       // {'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'}. Ex: ['fri', 'wed']
+ trigger_time: string               // format: %h:%m            (24-hour format) Ex: 05:05
+ duration: unsigned integer         // > 0
+ duration_unit: enum                // {'minutes', 'hours', 'days'}. Ex: 'days'
+ trigger_identifiers: [string]      // `uuid4` strings. Ex: ['ac97682c-c81e-4170-bb46-8301df317587', 'c28288c0-e24c-4a02-b047-c807bd6df3cc']
Output:
1) HTTP 200      // OK
status: 200
json: {}
2) HTTP 400      // Invalid parameters
status: 400
json: {
    "errors": [
        {"start_datetime": "Give the reason here"},       // Optional; only included when "start_datetime" has an error
        {"days": "Give another reason here"},             // As needed; only included when "days" has an error
        ...                                               // As needed...as there are other errors as well
    ]
}

// Sending a trigger
HTTP: POST
URL: '/bod/trigger'
Input:
+ trigger_identifier: string        // `uuid4` string. Ex: 'c28288c0-e24c-4a02-b047-c807bd6df3cc'
Output:
1) HTTP 200      // OK
status: 200
json: {}
2) HTTP 400      // Invalid parameter
status: 400
json: {
    "errors": [
        {"trigger_identifier": "Unable to find the given trigger identifier"}       // Only when invalid `trigger_identifier` is given
    ]
}


+ denotes required field
- denotes optional field
| denotes an "or"

**Bug**:
When submitted jobid is duplicated.
It return 500 and {"message": "Internal Server Error"} before program adding a job by addjob() function!



curl -H "Content-Type: application/json" -X POST -d '{"name":"Good Evening", "day_of_week":"sun", "start_time":"17:17"}' http://localhost:5000/recurrence/create

**Read (List):**

curl http://localhost:5000/recurrence

**Update :**

curl -H "Content-Type: application/json" -X PUT -d '{"id": "dc3d9acb052e47c9be310253937d644e","name":"Good Night", "day_of_week":"mon,sun,sat", "start_time":"18:18"}' http://localhost:5000/recurrence/edit

**Delete:**

curl -H "Content-Type: application/json" -X DELETE -d '{"id": "d345afd9d2ba4a3b924179fe87cdeda4"}' http://localhost:5000/recurrence/delete
