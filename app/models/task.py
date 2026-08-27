from datetime import datetime, date
from sqlalchemy import String, DateTime, func, Date, ForeignKey
from sqlalchemy import Enum as SQENum
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False,index=True)
    title: Mapped[str] = mapped_column(String(200),nullable=False)
    description: Mapped[str] = mapped_column(String(2000),nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SQENum(TaskStatus,name="task_status"),nullable=False,default=TaskStatus.PENDING)
    priority: Mapped[TaskPriority] = mapped_column(SQENum(TaskPriority,name="task_priority"),nullable=False,default=TaskPriority.MEDIUM)
    due_date: Mapped[date | None] = mapped_column(Date,nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    user: Mapped["User"] = relationship(back_populates="tasks")

