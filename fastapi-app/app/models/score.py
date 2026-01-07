from pydantic import BaseModel
from typing import Optional

class Score(BaseModel):
    id: Optional[int] = None  # Auto-increment ID
    student_id: int
    course_id: int
    score: float