"""Archivo main"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as api_router

app = FastAPI()
origin = [
    'http://localhost',
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods={"*"},
    allow_headers={"*"}
)

app.include_router(api_router)
