from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from typing import List
from app.models import Task, TaskCreate
from app.database import get_session

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
def get_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()

@router.post("/tasks", response_model=Task)
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    task = Task.from_orm(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    session.delete(task)
    session.commit()
    return {"message": "Tarefa deletada com sucesso"}

@router.patch("/tasks/{task_id}/toggle")
def toggle_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task.isCompleted = not task.isCompleted
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
