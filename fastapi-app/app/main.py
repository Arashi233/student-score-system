from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import User
from app.models.student import Student
from app.models.course import Course
from app.models.score import Score
from app.routes import user, students, courses, scores

app = FastAPI()

# 添加CORS中间件
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(user.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(courses.router, prefix="/api")
app.include_router(scores.router, prefix="/api")

# MongoDB配置
DATABASE_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(DATABASE_URL)
db = client.student_management

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = client
    app.mongodb = db

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
async def root():
    return {"message": "Student Management System API"}