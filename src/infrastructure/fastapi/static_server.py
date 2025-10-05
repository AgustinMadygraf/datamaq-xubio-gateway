"""
Path: src/infrastructure/fastapi/static_server.py
"""
from fastapi import FastAPI
from src.infrastructure.fastapi.dinamic_server import router as xubio_router

app = FastAPI()
app.include_router(xubio_router)
