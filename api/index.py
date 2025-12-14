from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi.middleware.cors import CORSMiddleware
import os

# --- Configuração do Banco de Dados ---
DATABASE_URL = os.environ.get("POSTGRES_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL não está configurada!")

# Ajuste necessário para Vercel Postgres (usa postgresql:// em vez de postgres://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

# Criar tabelas na primeira requisição
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Configuração de CORS - Permite todos os domínios da Vercel
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://practice-with-react-uqap.vercel.app",
    "https://*.vercel.app",  # Permite qualquer subdomínio da Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique apenas os domínios necessários
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de Dados (SQLModel) ---
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

# --- Rotas (Endpoints) ---

@app.get("/")
@app.get("/api")
def read_root():
    return {"message": "API de Tarefas rodando na Vercel!"}

@app.get("/api/tasks", response_model=List[Task])
def get_tasks(session: Session = Depends(get_session)):
    """Retorna todas as tarefas do banco"""
    tasks = session.exec(select(Task)).all()
    return tasks

@app.post("/api/tasks", response_model=Task)
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    """Cria uma nova tarefa no banco"""
    task = Task.model_validate(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Deleta uma tarefa pelo ID"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    session.delete(task)
    session.commit()
    return {"message": "Tarefa deletada com sucesso"}

@app.patch("/api/tasks/{task_id}/toggle")
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

# Handler para Vercel
handler = app
