"""Archivo main"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as api_router
from core.var_env import PRO_URI

app = FastAPI()
origin = [
    'http://localhost',
    'http://localhost:5173',
    PRO_URI
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods={"*"},
    allow_headers={"*"}
)

app.include_router(api_router)
