from fastapi import APIRouter,HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskStatus, TaskPriority
from sqlalchemy import select

router = APIRouter(prefix="/tasks",tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("",response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(user_id=1,title=task_data.title,description=task_data.description,status=task_data.status,priority=task_data.priority,due_date=task_data.due_date)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("",response_model=list[TaskResponse],status_code=status.HTTP_200_OK)
def get_tasks(page: int = Query(default=1,ge=1), limit: int = Query(default=10,ge=1,le=100),status: TaskStatus | None = None, priority: TaskPriority | None = None, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    statement = select(Task).where(Task.user_id == 1)
    if status is not None:
        statement = statement.where(Task.status == status)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    statement = statement.order_by(Task.created_at.desc()).offset(offset).limit(limit)
    result = db.execute(statement)
    tasks = result.scalars().all()
    return tasks

@router.get("/{task_id}",response_model=TaskResponse,status_code=status.HTTP_200_OK)
def get_task(task_id:int, db: Session = Depends(get_db)):
    statement = select(Task).where(Task.user_id==1,Task.id==task_id)
    result = db.execute(statement)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404,detail="Task Not Found")
    return task

@router.patch("/{task_id}",response_model=TaskResponse,status_code=status.HTTP_200_OK)
def update_task(task_id: int,task_data: TaskUpdate , db: Session = Depends(get_db)):
    statement = select(Task).where(Task.user_id == 1, Task.id == task_id)
    result = db.execute(statement)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task,field,value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    statement = select(Task).where(Task.user_id==1,Task.id==task_id)
    result = db.execute(statement)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "task deleted successfully"}



