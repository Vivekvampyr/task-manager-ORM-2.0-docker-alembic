from fastapi import APIRouter,HTTPException, Depends, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskStatus, TaskPriority, TaskListResponse
from sqlalchemy import select
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks",tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("",response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = Task(user_id=current_user.id,title=task_data.title,description=task_data.description,status=task_data.status,priority=task_data.priority,due_date=task_data.due_date)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("",response_model=TaskListResponse, status_code=status.HTTP_200_OK)
def get_tasks(page: int = Query(default=1,ge=1), limit: int = Query(default=10,ge=1,le=100),status: TaskStatus | None = None, priority: TaskPriority | None = None, search: str | None = Query(default=None,min_length=1,max_length=100),current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(Task).where(Task.user_id == current_user.id)
    if status is not None:
        statement = statement.where(Task.status == status)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    if search is not None:
        statement = statement.where(Task.title.ilike(f"%{search}%"))

    count_statement = select(func.count()).select_from(statement.subquery())
    total = db.scalar(count_statement) or 0
    
    offset = (page - 1) * limit
    statement = statement.order_by(Task.created_at.desc()).offset(offset).limit(limit)
    result = db.execute(statement)
    tasks = result.scalars().all()
    pages = ((total + limit - 1) // limit if total > 0 else 0)
    return TaskListResponse(items=tasks,page=page,limit=limit,total=total,pages=pages)

@router.get("/{task_id}",response_model=TaskResponse,status_code=status.HTTP_200_OK)
def get_task(task_id:int,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(Task).where(Task.user_id==current_user.id,Task.id==task_id)
    result = db.execute(statement)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404,detail="Task Not Found")
    return task

@router.patch("/{task_id}",response_model=TaskResponse,status_code=status.HTTP_200_OK)
def update_task(task_id: int,task_data: TaskUpdate ,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(Task).where(Task.user_id == current_user.id, Task.id == task_id)
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
def delete_task(task_id: int,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(Task).where(Task.user_id==current_user.id,Task.id==task_id)
    result = db.execute(statement)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "task deleted successfully"}



