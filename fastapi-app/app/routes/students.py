from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.student import Student
from typing import List

router = APIRouter()

# MongoDB
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["kadai"]
students_collection = db["student"]
counters_collection = db["counters"]

async def get_next_sequence_value(sequence_name: str) -> int:
    result = await counters_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True,
    )
    return result["sequence_value"]


# =========================
# Helper
# =========================
def student_helper(student: dict) -> dict:
    return {
        "id": student.get("id"),
        "name": student.get("name"),
        "sex": student.get("sex"),
        "status": student.get("status"),
    }


@router.get("/students", response_model=List[dict])
async def get_students():
    students = []
    async for s in students_collection.find({"status": 1}):
        students.append(student_helper(s))
    return students


@router.get("/studentsById/{student_id}")
async def get_student_by_id(student_id: int):
    student = await students_collection.find_one({"id": student_id, "status": 1})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_helper(student)


@router.get("/studentsByName/{student_name}")
async def get_student_by_name(student_name: str):
    student = await students_collection.find_one({"name": student_name, "status": 1})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_helper(student)


@router.post("/students")
async def create_student(student: Student):
    # 如果没传 id → 自动生成
    if student.id is None:
        student.id = await get_next_sequence_value("student_id")

    # 检查重复
    exists = await students_collection.find_one({"id": student.id})
    if exists:
        raise HTTPException(status_code=400, detail="学籍番号が既に存在します")

    student_dict = student.model_dump()
    await students_collection.insert_one(student_dict)

    return {
        "message": "Student created",
        "student": student_helper(student_dict),
    }


@router.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    update_data = student.model_dump(exclude={"id"})

    result = await students_collection.update_one(
        {"id": student_id},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="学籍番号が見つかりません")

    updated = await students_collection.find_one({"id": student_id})
    return {
        "message": f"Student {student_id} updated",
        "student": student_helper(updated),
    }


@router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    result = await students_collection.update_one(
        {"id": student_id},
        {"$set": {"status": 2}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="学籍番号が見つかりません")

    return {"message": f"Student {student_id} status updated to INACTIVE"}
