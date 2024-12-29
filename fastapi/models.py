from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    enrollments = relationship("Enrollment", back_populates="student")




class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    enrollments = relationship("Enrollment", back_populates="course")




class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(TIMESTAMP, default=datetime.utcnow)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")





class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    
