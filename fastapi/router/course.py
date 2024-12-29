from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel, EmailStr
from datetime import date


router=APIRouter(tags=['Course To Enroll'])

class course(BaseModel):
    name: str
    description: str
   

@router.post('/course')
def create_course(course : course, db:Session= Depends(get_db)):
    db_course = models.Course(name=course.name, description=course.description)

    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get('/course/{id}')
def get_couses(id: int, db: Session = Depends(get_db)):
    get_course = db.query(models.Course).filter(models.Course.id == id).first()
    if not get_course:
        raise HTTPException (status_code=404, detail="Course not found")
    else:
        return get_course




@router.get('/course')
def get_all_courses(db:Session= Depends(get_db)):
    return db.query(models.Course).all()


@router.put('/course/{id}')
def update_course(id:int, course: course, db: Session= Depends(get_db)):
    get_course = db.query(models.Course).filter(models.Course.id == id).first()
    if not get_course:
        raise HTTPException (status_code=404, detail="Course not found")
    else:
        get_course.name = course.name
        get_course.description = course.description
        db.commit()
        db.refresh(get_course)
        return get_course
    

@router.delete('/course/{id}')
def delete_course(id: int, db:Session= Depends(get_db)):
    delete_user= db.query(models.Course).filter(models.Course.id == id).delete()
    db.commit()
    return {"message": "Course deleted"}
