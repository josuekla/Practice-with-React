from sqlmodel import SQLModel, Session, create_engine
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL não configurada!")

# Ajuste para Vercel/Supabase (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Limpa a URL removendo parâmetros problemáticos e adiciona sslmode se necessário
def clean_database_url(url):
    parsed = urlparse(url)
    
    # Pega os parâmetros existentes
    params = parse_qs(parsed.query)
    
    # Remove parâmetros que podem causar problemas
    params_to_remove = ['supa', 'options', 'schema']
    for param in params_to_remove:
        params.pop(param, None)
    
    # Adiciona sslmode se não existir (necessário para Supabase)
    if 'sslmode' not in params:
        params['sslmode'] = ['require']
    
    # Reconstrói a URL
    new_query = urlencode(params, doseq=True)
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)

DATABASE_URL = clean_database_url(DATABASE_URL)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def create_db_and_tables():
    from app.models import Task  # Import aqui pra evitar circular import
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session