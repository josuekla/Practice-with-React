from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from typing import List, Optional
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de teste básica - não usa banco
@app.get("/")
@app.get("/api")
def root():
    return {"status": "ok", "message": "API funcionando!"}

@app.get("/debug")
@app.get("/api/debug")
def debug():
    """Mostra variáveis de ambiente disponíveis"""
    db_url = os.environ.get("DATABASE_URL", "NÃO ENCONTRADA")
    postgres_url = os.environ.get("POSTGRES_URL", "NÃO ENCONTRADA")
    
    # Esconde a senha
    if db_url != "NÃO ENCONTRADA":
        db_url = db_url[:30] + "..." if len(db_url) > 30 else db_url
    if postgres_url != "NÃO ENCONTRADA":
        postgres_url = postgres_url[:30] + "..." if len(postgres_url) > 30 else postgres_url
    
    return {
        "DATABASE_URL": db_url,
        "POSTGRES_URL": postgres_url,
        "all_env_keys": [k for k in os.environ.keys() if "VERCEL" in k or "DATABASE" in k or "POSTGRES" in k]
    }

# --- Banco de Dados (só carrega quando precisar) ---
engine = None

def get_engine():
    global engine
    if engine is None:
        from sqlmodel import create_engine
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
        if not url:
            raise Exception("DATABASE_URL não configurada")
        
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        
        # Limpa URL
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        for p in ['supa', 'options', 'schema']:
            params.pop(p, None)
        if 'sslmode' not in params:
            params['sslmode'] = ['require']
        url = urlunparse(parsed._replace(query=urlencode(params, doseq=True)))
        
        engine = create_engine(url, pool_pre_ping=True)
    return engine

def get_session():
    from sqlmodel import Session
    with Session(get_engine()) as session:
        yield session

# --- Modelos ---
from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    isCompleted: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default=None)

class TaskCreate(SQLModel):
    title: str
    description: str

# --- Rotas do Banco ---
@app.get("/health")
@app.get("/api/health")
def health():
    try:
        from sqlmodel import Session, text
        with Session(get_engine()) as session:
            session.exec(text("SELECT 1"))
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/tasks")
@app.get("/api/tasks")
def get_tasks(session = Depends(get_session)):
    from sqlmodel import select
    try:
        SQLModel.metadata.create_all(get_engine())
        return session.exec(select(Task)).all()
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/tasks")
@app.post("/api/tasks")
def create_task(task_in: TaskCreate, session = Depends(get_session)):
    try:
        SQLModel.metadata.create_all(get_engine())
        task = Task(
            title=task_in.title,
            description=task_in.description,
            isCompleted=False,
            created_at=datetime.utcnow()
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except Exception as e:
        raise HTTPException(500, str(e))

@app.delete("/tasks/{task_id}")
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Não encontrada")
    session.delete(task)
    session.commit()
    return {"ok": True}

@app.patch("/tasks/{task_id}/toggle")
@app.patch("/api/tasks/{task_id}/toggle")
def toggle_task(task_id: int, session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Não encontrada")
    task.isCompleted = not task.isCompleted
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Handler para Vercel Serverless
handler = Mangum(app, lifespan="off")
    return task

# Handler para Vercel
handler = app
