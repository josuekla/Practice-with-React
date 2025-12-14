from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.database import create_db_and_tables

app = FastAPI()

# Configuração de CORS
origins = [
    "https://practice-with-react-uqap.vercel.app",
    "https://practice-with-react-uqap.vercel.app/api",
    "https://practice-with-react-uqap.vercel.app/api/tasks",
    "http://localhost:5173",
    "http://localhost:5174", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()