from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routers import clientes  # 👈 importamos desde src

app = FastAPI(title="DataMaq Gateway")

# Montar carpeta estática y templates
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(clientes.router)
