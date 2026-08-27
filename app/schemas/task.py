from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict
from app.models.task import TaskPriority, TaskStatus

class TaskCreate(BaseModel):
    title: str = Field(min_length=3,max_length=200)
    description: str | None = Field(default=None,max_length=2000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: date | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: date | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None,min_length=3,max_length=200)
    description: str | None = Field(default=None,max_length=2000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: date | None = None

