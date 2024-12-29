from fastapi import APIRouter, Depends, HTTPException
from database import get_db
import models
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.sql import func


router=APIRouter(tags=['Enrollment'])


class enrollment(BaseModel):
    student_id: int 
    course_id: int
    enrolled_at: datetime



@router.post('/student/enrollment')
def student_enrolled(enrollment: enrollment, db: Session = Depends(get_db)):
        created_enrolled_student= models.Enrollment(student_id = enrollment.student_id, course_id= enrollment.course_id, enrolled_at= enrollment.enrolled_at )
        db.add(created_enrolled_student)
        db.commit()
        db.refresh(created_enrolled_student) 
        return created_enrolled_student


@router.get('/student/enrollment/{id}')
def get_enrolled_details(id: int, db:Session= Depends(get_db)):
      get_enrolled_details=db.query(models.Enrollment).filter(models.Enrollment.id == id).first()
      if not get_enrolled_details:
        raise HTTPException (status_code=400, detail="Enrolled id not found")
      else:
           return get_enrolled_details



# @router.put('student/course/{id}')
# def update_enrolled_details(id: int, enrollment: enrollment, db:Session=Depends(get_db)):
#      update_enrolled_details=db.query(models.Enrollment).filter(models.Enrollment.id == id).first()
#      if not update_enrolled_details:
#           raise HTTPException(status_code=400, detail="Enrolled id not found")
#      else:
#           update_enrolled_details.student_id=enrollment.student_id
#           update_enrolled_details.course_id=enrollment.course_id
#           update_enrolled_details.enrolled_at=enrollment.enrolled_at
#           return update_enrolled_details
     

@router.get('/student/enrollment')
def get_all(db:Session= Depends(get_db)):
     get_all=db.query(models.Enrollment).count()
     if not get_all:
          raise HTTPException(status_code=400, detail="No enrolled students found")
     else:
        return get_all



@router.delete('/student/enrollment/{id}')
def delete_enrolled_details(id: int, db: Session= Depends(get_db)):
     delete_enrolled_details=db.query(models.Enrollment).filter(models.Enrollment.id == id).first()
     if not delete_enrolled_details:
          raise HTTPException(status_code=400, detail="Enrolled id not found")
     else:
          db.delete(delete_enrolled_details)
          db.commit()
          return {"Enrolled User deleted Successfully"}
     

