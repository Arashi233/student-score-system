from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
import hashlib
import secrets
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import User as UserModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# MongoDB configuration
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["kadai"]
users_collection = db["user"]
counters_collection = db["counters"]

# Helper function to get next sequence value
async def get_next_sequence_value(sequence_name: str) -> int:
    result = await counters_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    
    if not result:
        await counters_collection.insert_one({"_id": sequence_name, "sequence_value": 1})
        return 1
    
    return result["sequence_value"]

class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: str
    type: int
    name: str

class LoginResponse(BaseModel):
    token: str
    user: User

def hash_password(password: str) -> str:
    """简单的密码哈希函数（实际项目应使用更安全的方法）"""
    return hashlib.md5(password.encode()).hexdigest()

# Initialize default users if not exists
async def init_default_users():
    # Check if users collection is empty
    count = await users_collection.count_documents({})
    if count == 0:
        # Add default users with auto-increment IDs
        default_users = [
            {"type": 1, "name": "1", "pwd": "1"},  # 普通用户
            {"type": 2, "name": "2", "pwd": "2"},      # 管理用户
            {"type": 3, "name": "3", "pwd": "3"}   # 超级用户
        ]
        
        for user_data in default_users:
            next_id = await get_next_sequence_value("user_id")
            user_data["id"] = next_id
            await users_collection.insert_one(user_data)

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    # Initialize default users if collection is empty
    await init_default_users()
    
    # Find user by name
    user = await users_collection.find_one({"name": login_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # Check password (note: plain text for demo, use hashing in production)
    if user["pwd"] != login_data.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # Generate token
    token = secrets.token_hex(32)
    return {
        "token": token,
        "user": {
            "id": str(user["id"]),  # Convert to string for consistency
            "type": user["type"],
            "name": user["name"]
        }
    }

# Add new endpoint to create users with auto-increment ID
@router.post("/users", response_model=User)
async def create_user(user: UserModel):
    # If ID is not provided, generate auto-increment ID
    if user.id is None:
        next_id = await get_next_sequence_value("user_id")
        user.id = next_id
    
    # Check if ID already exists
    exists = await users_collection.find_one({"id": user.id})
    if exists:
        raise HTTPException(status_code=400, detail="用户IDが既に存在します")
    
    # Check if username already exists
    name_exists = await users_collection.find_one({"name": user.name})
    if name_exists:
        raise HTTPException(status_code=400, detail="用户名が既に存在します")
    
    # Insert user into database
    user_dict = user.dict()
    await users_collection.insert_one(user_dict)
    
    # Return created user
    return User(
        id=str(user.id),
        type=user.type,
        name=user.name
    )

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):

    return {"message": "User info endpoint", "token": token}