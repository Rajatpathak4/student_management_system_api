from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel, EmailStr
from datetime import datetime, date



router=APIRouter(tags=['Students'])


class student(BaseModel):
    name: str
    email: EmailStr
    dob: date
    gender: str
    address: str


@router.post('/student')
def create_student(student: student, db: Session= Depends(get_db)):
    create_user= models.Student(name= student.name, email= student.email, dob= student.dob, gender=student.gender, address= student.address)
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user


@router.get('/student{id}')
def get_student(id: int, db: Session= Depends(get_db)):
    existing_user= db.query(models.Student).filter(models.Student.id == id).first()
    if not existing_user:
        raise HTTPException (status_code=400, detail="Invalid student")
    else:
        return existing_user
    

@router.put('/student/{id}', response_model=student)
def update_student(id: int, student: student ,db: Session= Depends(get_db)):
    update_student=db.query(models.Student).filter(models.Student.id == id).first()
    if not update_student:
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        update_student.name=student.name
        update_student.email=student.email
        update_student.dob=student.dob
        update_student.gender=student.gender
        update_student.address=student.address
        db.commit()
        db.refresh(update_student)
    return update_student




@router.delete('/student/{id}')
def delete_user(id: int , db: Session= Depends(get_db)):
    delete_user=db.query(models.Student).filter(models.Student.id == id).delete()
    if not delete_user:
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        db.commit()
        return {"message": "Student deleted successfully"}
    



@router.get('/student')
def get_all_student(db:Session= Depends(get_db)):
    return db.query(models.Student).all()


    
    







