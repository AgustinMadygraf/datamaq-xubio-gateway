from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from database import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/clientes")
async def clientes(request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, email, cuit, telefono, direccion FROM clientes ORDER BY nombre")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes})
