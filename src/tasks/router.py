from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..auth.router import get_current_user # We will create this next

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Create the task and link it to the logged-in user's ID
    new_task = models.Task(**task.dict(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[schemas.Task])
def get_user_tasks(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Only fetch tasks that belong to the current user
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()