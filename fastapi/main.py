from fastapi import FastAPI
import models
from database import engine
from router import student, course, enrollment, user
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

models.Student.metadata.create_all(bind=engine)


app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)
app.include_router(user.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)