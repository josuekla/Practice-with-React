from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import traceback

app = FastAPI()

# Configuração de CORS - permite tudo para debug
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuração do Banco de Dados ---
engine = None

def get_database_url():
    """Obtém e limpa a URL do banco"""
    url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
    
    if not url:
        return None
    
    # Corrige protocolo
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    
    # Remove parâmetros problemáticos e adiciona sslmode
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    for param in ['supa', 'options', 'schema']:
        params.pop(param, None)
    
    if 'sslmode' not in params:
        params['sslmode'] = ['require']
    
    new_query = urlencode(params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def get_engine():
    global engine
    if engine is None:
        from sqlmodel import create_engine
        url = get_database_url()
        if not url:
            raise Exception("DATABASE_URL não configurada!")
        engine = create_engine(url, pool_pre_ping=True)
    return engine

def get_session():
    from sqlmodel import Session
    with Session(get_engine()) as session:
        yield session

# --- Modelos ---
from sqlmodel import SQLModel, Field
from datetime import datetime

def get_brazil_time():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/Sao_Paulo"))
    except:
        return datetime.utcnow()

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    isCompleted: bool = Field(default=False)
    created_at: datetime = Field(default_factory=get_brazil_time)

class TaskCreate(SQLModel):
    title: str
    description: str

# --- Rotas ---

@app.get("/")
@app.get("/api")
def read_root():
    url = get_database_url()
    return {
        "message": "API rodando!",
        "database_configured": url is not None,
        "env_vars": list(os.environ.keys())  # Debug: mostra variáveis disponíveis
    }

@app.get("/health")
@app.get("/api/health")
def health():
    try:
        from sqlmodel import Session, text
        with Session(get_engine()) as session:
            session.exec(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e), "traceback": traceback.format_exc()}

@app.get("/tasks", response_model=List[Task])
@app.get("/api/tasks", response_model=List[Task])
def get_tasks(session = Depends(get_session)):
    try:
        from sqlmodel import select
        SQLModel.metadata.create_all(get_engine())
        return session.exec(select(Task)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.post("/tasks", response_model=Task)
@app.post("/api/tasks", response_model=Task)
def create_task(task_in: TaskCreate, session = Depends(get_session)):
    try:
        SQLModel.metadata.create_all(get_engine())
        task = Task(
            title=task_in.title,
            description=task_in.description,
            isCompleted=False,
            created_at=get_brazil_time()
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.delete("/tasks/{task_id}")
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    session.delete(task)
    session.commit()
    return {"message": "Deletada"}

@app.patch("/tasks/{task_id}/toggle")
@app.patch("/api/tasks/{task_id}/toggle")
def toggle_task(task_id: int, session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task.isCompleted = not task.isCompleted
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Handler Vercel
handler = app
    return task

# Handler para Vercel
handler = app
