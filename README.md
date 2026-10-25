# Students CRUD - EWB Internship
Mandatory Core with DOB field

## Run
pip install -r requirements.txt
uvicorn main:app --reload

## Test
Open http://127.0.0.1:8000/docs
Endpoints:
- POST /students
- GET /students
- GET /students/{id}
- PUT /students/{id}
- DELETE /students/{id}