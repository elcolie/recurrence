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
+ days: [enum]                       // {'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'}. Ex: ['fri', 'wed']
+ trigger_time: string               // format: %h:%m   //python = %H:%i         (24-hour format) Ex: 05:05
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

+ denotes required field
- denotes optional field
| denotes an "or"

**Delete:**
HTTP : DELETE
URL: '/recurrence/days'
Input:
+ id: string        // `uuid4` string. Ex: 'c28288c0-e24c-4a02-b047-c807bd6df3cc'
Output:
1) HTTP 200     // OK
status: 200
json: {}
2) HTTP 400
status : 400    // Invalid parameter. id is missing
3) HTTP 410
status : 410
json: { error description } //job id is gone.


Schedule a trigger (REST API)
HTTP: POST
URL: '/recurrence/dates'
Input:
+ start_date: string             // format: %Y-%m-%d (24-hour format). Ex: 2009-09-09
+ dates: [enum]                       // Ex: ['1','11','21','31']
+ trigger_time: string               // format: %h:%m   //python = %H:%i         (24-hour format) Ex: 05:05
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

+ denotes required field
- denotes optional field
| denotes an "or"

**Delete:**
HTTP : DELETE
URL: '/recurrence/days'
Input:
+ id: string        // `uuid4` string. Ex: 'c28288c0-e24c-4a02-b047-c807bd6df3cc'
Output:
1) HTTP 200     // OK
status: 200
json: {}
2) HTTP 400
status : 400    // Invalid parameter. id is missing
3) HTTP 410
status : 410
json: { error description } //job id is gone.



// Sending a trigger to server.
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


**Warning**:
When submitted duplicated job id.
It return 500 and {"message": "Internal Server Error"} before program adding a job by addjob() function!


**Read (All list : Debugging URL):**
Get all the job list in the scheduler.
HTTP: GET
URL: '/debugging'
Output:
1. list of job instance and notify line. Order by `next run`.
2. `workfile.txt` It is safe to delete.
