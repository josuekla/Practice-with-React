from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os

app = FastAPI()


origins = [
    "https://practice-with-react-uqap.vercel.app",
    "http://localhost:5173",
    "http://localhost:5174",  # adicione a porta correta
]

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuração do Banco de Dados (Lazy Loading) ---
engine = None
DATABASE_URL = None

def clean_database_url(url):
    """Limpa a URL do banco removendo parâmetros problemáticos"""
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    # Remove parâmetros que podem causar problemas
    for param in ['supa', 'options', 'schema']:
        params.pop(param, None)
    
    # Adiciona sslmode se não existir
    if 'sslmode' not in params:
        params['sslmode'] = ['require']
    
    new_query = urlencode(params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def get_engine():
    global engine, DATABASE_URL
    if engine is None:
        from sqlmodel import create_engine
        
        DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
        
        if not DATABASE_URL:
            raise Exception("DATABASE_URL não configurada!")
        
        # Corrige protocolo para SQLAlchemy
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
        # Limpa a URL
        DATABASE_URL = clean_database_url(DATABASE_URL)
        
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return engine

def get_session():
    from sqlmodel import Session
    with Session(get_engine()) as session:
        yield session

# --- Modelos de Dados ---
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

# --- Criar tabelas ---
tables_created = False

def ensure_tables():
    global tables_created
    if not tables_created:
        SQLModel.metadata.create_all(get_engine())
        tables_created = True

# --- Rotas ---

@app.get("/")
@app.get("/api")
def read_root():
    """Rota de teste - verifica se a API está rodando"""
    db_status = "não configurado"
    try:
        url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
        if url:
            db_status = "configurado ✓"
    except:
        pass
    return {
        "message": "API de Tarefas rodando!",
        "database": db_status
    }

@app.get("/api/health")
@app.get("/health")
def health_check():
    """Verifica conexão com banco"""
    try:
        from sqlmodel import Session, text
        with Session(get_engine()) as session:
            session.exec(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/api/tasks", response_model=List[Task])
@app.get("/tasks", response_model=List[Task])
def get_tasks(session = Depends(get_session)):
    """Retorna todas as tarefas"""
    from sqlmodel import select
    ensure_tables()
    tasks = session.exec(select(Task)).all()
    return tasks

@app.post("/api/tasks", response_model=Task)
@app.post("/tasks", response_model=Task)
def create_task(task_in: TaskCreate, session = Depends(get_session)):
    """Cria uma nova tarefa"""
    ensure_tables()
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

@app.delete("/api/tasks/{task_id}")
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session = Depends(get_session)):
    """Deleta uma tarefa pelo ID"""
    ensure_tables()
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    session.delete(task)
    session.commit()
    return {"message": "Tarefa deletada com sucesso"}

@app.patch("/api/tasks/{task_id}/toggle")
@app.patch("/tasks/{task_id}/toggle")
def toggle_task(task_id: int, session = Depends(get_session)):
    """Marca/Desmarca uma tarefa como completa"""
    ensure_tables()
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
