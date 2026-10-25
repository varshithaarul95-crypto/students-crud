from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3

app = FastAPI(title="Students CRUD - EWB Internship")

def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
conn.execute('''CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    dob TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    course TEXT,
    address TEXT,
    enrollment_date TEXT
)''')
conn.commit()
conn.close()

class StudentCreate(BaseModel):
    student_id: str
    name: str
    dob: str
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None

class Student(StudentCreate):
    pass

@app.post("/students", response_model=Student)
def create_student(s: StudentCreate):
    conn = get_db()
    try:
        conn.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?)",
        (s.student_id, s.name, s.dob, s.email, s.phone, s.course, s.address, s.enrollment_date))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="student_id already exists")
    finally:
        conn.close()
    return s

@app.get("/students", response_model=List[Student])
def list_students(name: Optional[str] = None, course: Optional[str] = None):
    conn = get_db()
    query = "SELECT * FROM students WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if course:
        query += " AND course LIKE ?"
        params.append(f"%{course}%")
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Student not found")
    return dict(row)

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: str, s: StudentCreate):
    conn = get_db()
    row = conn.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    conn.execute("UPDATE students SET name=?, dob=?, email=?, phone=?, course=?, address=?, enrollment_date=? WHERE student_id=?",
    (s.name, s.dob, s.email, s.phone, s.course, s.address, s.enrollment_date, student_id))
    conn.commit()
    conn.close()
    return s

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    conn = get_db()
    cur = conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Deleted successfully"}