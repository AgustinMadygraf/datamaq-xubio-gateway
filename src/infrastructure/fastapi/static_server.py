import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from src.infrastructure.fastapi.dinamic_server import router as xubio_router

app = FastAPI()
app.include_router(xubio_router)

# Usar ruta absoluta o relativa correcta para la carpeta static
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../static")
static_dir = os.path.normpath(static_dir)

app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/")
def root():
    "Redirige la raíz a /static/index.html"
    return RedirectResponse(url="/static/index.html")
