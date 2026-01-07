from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.course import Course
from bson import ObjectId

router = APIRouter()
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["kadai"]
courses_collection = db["course"]
counters_collection = db["counters"]

# Helper function to get next sequence value
async def get_next_sequence_value(sequence_name: str) -> int:
    # Try to update the counter
    result = await counters_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    
    # If counter doesn't exist, create it
    if not result:
        await counters_collection.insert_one({"_id": sequence_name, "sequence_value": 1})
        return 1
    
    return result["sequence_value"]

def course_helper(course) -> dict:
    return {
        "id": course["id"],   # ⭐修正：使用我们生成的整数ID
        "name": course["name"],
    }
@router.get("/")
@router.get("/courses")
async def get_courses():
    courses = []
    async for d in courses_collection.find():
        courses.append(course_helper(d))
    return courses  

@router.get("/courseById/{course_id}")
async def get_course_by_id(course_id: int):
    course = await courses_collection.find_one({"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_helper(course)

@router.get("/courseByName/{course_name}")
async def get_course_by_name(course_name: str):
    course = await courses_collection.find_one({"name": course_name})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_helper(course)

@router.post("/courses")
async def create_course(course: Course):
    # If ID is not provided, generate auto-increment ID
    if course.id is None:
        # Get next sequence value for courses
        next_id = await get_next_sequence_value("course_id")
        course.id = next_id
    
    # Check if ID already exists
    exists = await courses_collection.find_one({"id": course.id})
    if exists:
        raise HTTPException(status_code=400, detail="科目IDが既に存在します")
    
    # Check if course name already exists (optional but recommended)
    name_exists = await courses_collection.find_one({"name": course.name})
    if name_exists:
        raise HTTPException(status_code=400, detail="科目名が既に存在します")
    
    course_dict = course.dict()
    await courses_collection.insert_one(course_dict)
    return {"message": "Course created", "course": course_helper(course_dict)}

@router.put("/courses/{course_id}")
async def update_course(course_id: int, course: Course):
    # 更新科目信息
    result = await courses_collection.update_one({"id": course_id}, {"$set": course.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": f"Course {course_id} updated", "course": course_helper(course)}