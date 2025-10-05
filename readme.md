# DataMaq Xubio Gateway

Gateway FastAPI para interactuar con la API de Xubio usando OAuth2 client credentials.

## Características

- Endpoints para obtener token y listar clientes de Xubio.
- Pronto: endpoints para stock, inventario, presupuesto, listado de precios, etc.
- Configuración por variables de entorno (`.env`).
- Logging colorido estilo Flask.
- Arranque sencillo con Uvicorn.
- Uso de entorno virtual recomendado (`python -m venv venv`).

## Instalación

1. Clona el repo.
2. Crea un entorno virtual y actívalo:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```
3. Instala dependencias:
   ```sh
   pip install -r requirements.txt
   ```
4. Copia `.env.example` a `.env` y completa tus credenciales Xubio.

## Uso

Arranca el servidor:
```sh
python run.py
```
Por defecto corre en `http://0.0.0.0:5000`.

### Endpoints principales

- `POST /api/xubio/token/test`: Prueba de obtención de token.
- `GET /api/xubio/clientes`: Lista clientes de Xubio (parámetro opcional `updated_since`).
- Próximamente: endpoints de stock, inventario, presupuesto, listado de precios, etc.

## Configuración

Variables en `.env`:
- `XUBIO_BASE_URL`
- `XUBIO_TOKEN_URL`
- `XUBIO_CLIENT_ID`
- `XUBIO_CLIENT_SECRET`
- `XUBIO_TIMEOUT_S`
- `XUBIO_VERIFY_TLS`
- `XUBIO_CLIENTS_PATH`
- `LOG_LEVEL`
