from sqlmodel import SQLModel, Field
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

def get_brazil_time():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    isCompleted: bool = Field(default=False)
    created_at: datetime = Field(default_factory=get_brazil_time, nullable=False)

class TaskCreate(SQLModel):
    title: str
    description: str
