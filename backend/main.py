from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Optional
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from fastapi.middleware.cors import CORSMiddleware
import os

# --- Configuração do Banco de Dados ---
# Verifica se existe uma variável de ambiente DATABASE_URL (usada no Docker)
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Se estivermos no Docker, usamos Postgres
    engine = create_engine(DATABASE_URL)
else:
    # Se estivermos rodando localmente, usamos SQLite
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

# Evento que roda quando a API inicia
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Configuração de CORS
origins = [
    "https://practice-with-react-uqap.vercel.app",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de Dados (SQLModel) ---
# Função auxiliar para pegar a hora no Brasil
def get_utc_time():
    return datetime.now(timezone.utc)

# Agora a classe Task é uma Tabela no banco!
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    isCompleted: bool = Field(default=False)
    created_at: datetime = Field(
    default_factory=get_utc_time,
    nullable=False
)

# Modelo apenas para receber dados (sem ID, pois o banco gera)
class TaskCreate(SQLModel):
    title: str
    description: str

# --- Rotas (Endpoints) ---

@app.get("/")
def read_root():
    return {"message": "API de Tarefas com Banco de Dados!"}

@app.get("/tasks", response_model=List[Task])
def get_tasks(session: Session = Depends(get_session)):
    """Retorna todas as tarefas do banco"""
    tasks = session.exec(select(Task)).all()
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    """Cria uma nova tarefa no banco"""
    task = Task.from_orm(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Deleta uma tarefa pelo ID"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    session.delete(task)
    session.commit()
    return {"message": "Tarefa deletada com sucesso"}

@app.patch("/tasks/{task_id}/toggle")
def toggle_task(task_id: int, session: Session = Depends(get_session)):
    """Marca/Desmarca uma tarefa como completa"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    task.isCompleted = not task.isCompleted
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
