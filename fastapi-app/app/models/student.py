from pydantic import BaseModel
from enum import Enum
from typing import Optional

class StudentStatus(int, Enum):
    ACTIVE = 1
    INACTIVE = 2

class Student(BaseModel):
    id: Optional[int] = None  # 学籍番号 (auto-increment)
    name: str
    sex: str
    status: StudentStatus
