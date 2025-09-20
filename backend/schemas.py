from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Схемы для Course
class CourseBase(BaseModel):
    title: str
    description: str
    duration_hours: int = 0
    difficulty_level: str = "beginner"

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_hours: Optional[int] = None
    difficulty_level: Optional[str] = None

class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Схемы для Topic
class TopicBase(BaseModel):
    title: str
    description: str
    content: str
    order_index: int = 0
    duration_minutes: int = 0

class TopicCreate(TopicBase):
    course_id: int

class TopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    order_index: Optional[int] = None
    duration_minutes: Optional[int] = None

class Topic(TopicBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Схемы для Assignment
class AssignmentBase(BaseModel):
    title: str
    description: str
    instructions: str
    difficulty_level: str = "easy"
    estimated_hours: int = 1
    is_required: bool = True

class AssignmentCreate(AssignmentBase):
    topic_id: int

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_hours: Optional[int] = None
    is_required: Optional[bool] = None

class Assignment(AssignmentBase):
    id: int
    topic_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Схемы с вложенными объектами
class TopicWithAssignments(Topic):
    assignments: List[Assignment] = []

class CourseWithTopics(Course):
    topics: List[TopicWithAssignments] = []

# Схемы для Hint
class HintBase(BaseModel):
    text: str
    penalty: int = 10
    order_index: int = 0

class HintCreate(HintBase):
    assignment_id: int

class HintUpdate(BaseModel):
    text: Optional[str] = None
    penalty: Optional[int] = None
    order_index: Optional[int] = None

class Hint(HintBase):
    id: int
    assignment_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
