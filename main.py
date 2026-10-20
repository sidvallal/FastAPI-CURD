
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
from database import Base, engine, get_db
from schemas import StudentCreate, StudentUpdate, StudentResponse

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student CRUD API")


@app.get("/")
def home():
    return {"message": "Welcome to the Student CRUD API"}


# CREATE
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
):
    new_student = models.Student(**student.model_dump())
    db.add(new_student)

    try:
        db.commit()
        db.refresh(new_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
        )

    return new_student


# READ ALL
@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).order_by(models.Student.id).all()


# READ ONE
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# UPDATE
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated_data: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = db.get(models.Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    for field, value in updated_data.model_dump().items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
        )

    return student


# DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
