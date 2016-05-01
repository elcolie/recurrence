# recurrence
RESTful backend APIs UIH portal

## Normal run :
python recurrence.py

## Debuggin mode :
python recurrence.py debug

## CRUD
**Create :**
curl -H "Content-Type: application/json" -X POST -d '{"name":"Good Evening", "day_of_week":"sun", "start_time":"17:17"}' http://localhost:5000/recurrence/create

**Read (List):**
curl http://locahost:5000/recurrence

**Update :**
curl -H "Content-Type: application/json" -X POST -d '{"id": "dc3d9acb052e47c9be310253937d644e","name":"Good Night", "day_of_week":"mon,sun,sat", "start_time":"18:18"}' http://localhost:5000/recurrence/create

**Delete:**
curl -H "Content-Type: application/json" -X POST -d '{"id": "d345afd9d2ba4a3b924179fe87cdeda4"}' http://localhost:5000/recurrence/delete
