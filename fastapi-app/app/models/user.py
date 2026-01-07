from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None  # Auto-increment ID
    type: int  # 1: Student, 2: Admin, 3: Super Admin
    name: str
    pwd: str