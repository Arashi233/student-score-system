from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    id: Optional[int] = None  # Auto-increment ID
    name: str