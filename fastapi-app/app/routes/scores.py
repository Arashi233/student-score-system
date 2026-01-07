from fastapi import APIRouter, HTTPException, Depends
from app.models.score import Score
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

router = APIRouter()
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["kadai"]
scores_collection = db["score"]
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
def score_helper(score) -> dict:
    return {
        "id": score.get("id"),
        "student_id": score.get("student_id"),
        "course_id": score.get("course_id"),
        "score": score.get("score"),
    }

@router.get("/scores")
async def get_scores(student_id: int = None, course_id: int = None):
    # 获取成绩列表，支持按学号或科目筛选
    scores = []
    query = {}
    if student_id:
        query["student_id"] = student_id
    if course_id:
        query["course_id"] = course_id
    async for d in scores_collection.find(query):
        scores.append(score_helper(d))
    return scores

@router.post("/scores")
async def create_score(score: Score):
    # If ID is not provided, generate auto-increment ID
    if score.id is None:
        # Get next sequence value for scores
        next_id = await get_next_sequence_value("score_id")
        score.id = next_id
    
    # Check if ID already exists
    exists = await scores_collection.find_one({"id": score.id})
    if exists:
        raise HTTPException(status_code=400, detail="成績IDが既に存在します")
    
    # Check if this student-course combination already exists
    combination_exists = await scores_collection.find_one({
        "student_id": score.student_id,
        "course_id": score.course_id
    })
    if combination_exists:
        raise HTTPException(status_code=400, detail="この学生のこの科目の成績は既に存在します")
    
    score_dict = score.dict()
    await scores_collection.insert_one(score_dict)
    return {"message": "Score created", "score": score_helper(score_dict)}

@router.put("/scores/{score_id}")
async def update_score(score_id: int, score: Score):
    await scores_collection.update_one({"id": score_id}, {"$set": score.dict()})
    return {"message": f"Score {score_id} updated"}

@router.get("/scores/{score_id}")
async def get_score_by_id(score_id: int):
    # 根据ID获取单个成绩记录
    score = await scores_collection.find_one({"id": score_id})
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score_helper(score)

@router.delete("/scores/{score_id}")
async def delete_score(score_id: int):
    # 删除指定的成绩记录
    result = await scores_collection.delete_one({"id": score_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Score not found")
    return {"message": f"Score {score_id} deleted"}