# Validador Lingüístico Inteligente

Aplicación para validar palabras en español con un frontend Astro estático, un servidor Python ligero en el contenedor del frontend y un backend FastAPI dentro de Docker.

## Arquitectura actual

- `frontend`: construye Astro en modo estático con `pnpm build`.
- El contenedor del frontend ejecuta `frontend/server.py`, que sirve `dist/`.
- El frontend expone dos rutas internas:
  - `/backendapi/session`
  - `/backendapi/validate`
- Esas rutas se reenvían al backend en `http://backend:8000` dentro de la red `dicc-network`.
- El backend no publica su puerto al host.
- Los contenedores se llaman `frontend` y `backend`.

## Requisitos

- Python 3.12 o superior.
- Node.js 22.12 o superior.
- pnpm 10.
- Docker y Docker Compose si quieres levantar todo con contenedores.

## Variables de entorno

El archivo `.env` de la raíz solo controla el backend:

```env
FRONTEND_ORIGIN=https://scrae.scarpy.abrdns.com
SESSION_SECRET_KEY=your-long-random-secret
SESSION_TTL_SECONDS=3600
SESSION_COOKIE_SECURE=true
```

## Ejecutar con Docker

```powershell
docker compose up --build
```

Servicios:
- Frontend: `http://localhost:4321`
- Backend: no está publicado en el host; solo es accesible desde el frontend dentro de `dicc-network`.

## Desarrollo local

### Backend

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
pnpm install
pnpm build
python server.py
```

## Flujo de validación

1. El navegador carga la interfaz desde el frontend.
2. El frontend llama a `/backendapi/session`.
3. El servidor Python del frontend reenvía la petición a `http://backend:8000/api/session`.
4. El frontend llama a `/backendapi/validate`.
5. El servidor Python del frontend reenvía la validación a `http://backend:8000/api/validate`.

## Tests

### Backend

```powershell
cd backend
pytest
```

### Verificación rápida

```powershell
python -m compileall backend
python -m py_compile frontend/server.py
```

## Notas

- El frontend es estático, pero el contenedor incluye un servidor Python mínimo para reenviar las validaciones.
- No hay endpoint `/api` público en el frontend.
- La comunicación entre frontend y backend ocurre solo por Docker network.
