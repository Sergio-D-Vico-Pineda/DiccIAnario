# Validador Lingüístico Inteligente

Aplicación web para validar palabras en español con FastAPI, spaCy, Astro 6 y Tailwind CSS 4.

## Estructura


## Requisitos

- Python 3.12 o superior.
- Node.js 22.12.0 o superior.
- pnpm 8 o superior (o npm/yarn compatibles).
- Opcional: Docker y Docker Compose.

## Configuración local

El proyecto espera un archivo `.env` en la raíz del repositorio. Desde ahí se leen tanto las variables del backend como las del frontend.

### Variables de entorno requeridas

Copia `.env.example` a `.env` en la raíz del repositorio y configura:

```env
FRONTEND_ORIGIN=http://localhost:4321
PUBLIC_API_BASE_URL=http://localhost:8000
SESSION_SECRET_KEY=your-long-random-secret
SESSION_TTL_SECONDS=3600
SESSION_COOKIE_SECURE=false
```

**Importante**: `SESSION_SECRET_KEY` es privada y **nunca se expone al navegador**. Solo firma una cookie httpOnly con caducidad corta.

### 1. Backend

En PowerShell:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si vas a usar el modelo grande de spaCy que pide el proyecto, instálalo también:

```powershell
python -m spacy download es_core_news_lg
```

Si prefieres ajustar la configuración por archivo, copia `.env.example` a `.env` en la raíz del repositorio y modifica los valores que necesites.

Arranca la API:

```powershell
uvicorn app.main:app --reload --port 8000
```

La API quedará disponible en `http://localhost:8000`.

### 2. Frontend

En otra terminal:

```powershell
cd frontend
pnpm install
$env:PUBLIC_API_BASE_URL = "http://localhost:8000"
pnpm run dev
```

El frontend toma `PUBLIC_API_BASE_URL` desde el `.env` de la raíz. Si no está definido, usa `http://localhost:8000`.

La interfaz quedará disponible en `http://localhost:4321`.

## Cómo probar la app

1. Abre `http://localhost:4321` en el navegador.
2. Escribe una sola palabra, por ejemplo `corriendo`.
3. Pulsa `Validar`.
4. Revisa el resultado con lema, POS, clasificación y confianza del modelo.

La API usa una cookie de sesión firmada y de corta duración:

```powershell
Invoke-RestMethod `
	-Method Post `
	-Uri http://localhost:8000/api/session `
	-WebSession $session

Invoke-RestMethod `
	-Method Post `
	-Uri http://localhost:8000/api/validate `
	-WebSession $session `
	-ContentType "application/json" `
	-Body '{"term":"corriendo"}'
```

Si accedes desde el navegador en `http://localhost:4321`, la app crea la sesión automáticamente y luego envía las solicitudes con `credentials: include`.

## Seguridad: Cookie Firmada

La aplicación implementa una cookie de sesión firmada para que **el navegador no conozca ningún secreto reutilizable**:

### Arquitectura

1. **Frontend estático**: Solicita una sesión a `POST /api/session` y luego llama a `POST /api/validate` con `credentials: include`.
2. **Backend FastAPI**: Emite una cookie `httpOnly` firmada con expiración corta.
3. **Backend FastAPI**: Valida la cookie en cada petición protegida. Si es inválida o expirada, rechaza la solicitud con `401`.

### Por qué es seguro

- **El secreto nunca se expone al navegador**: No aparece en `localStorage`, `sessionStorage`, ni en el código HTML/JavaScript.
- **La cookie es `httpOnly`**: JavaScript no puede leerla ni copiarla.
- **Expira sola**: La cookie y el token firmado caducan automáticamente.
- **CORS con credenciales**: El backend solo permite el origen del frontend.

### Configuración en producción

En `docker-compose.yml`, asegúrate de usar variables de entorno en lugar de valores hardcodeados:

```yaml
environment:
  API_TOKEN: ${API_TOKEN:-your-secure-token-here}
```

Luego, al lanzar los contenedores, proporciona el token como variable de entorno:

```bash
API_TOKEN="tu-token-secreto-aqui" docker-compose up
```

## Tests

### Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

Si todavía no tienes `pytest` instalado en el entorno virtual, vuelve a ejecutar:

```powershell
pip install -r requirements.txt
```

### Verificación rápida de sintaxis

```powershell
python -m compileall backend
```

## Con Docker

Si prefieres levantar todo sin instalar dependencias locales:

```powershell
docker compose up --build
```

- Frontend: `http://localhost:4321`
- Backend: `http://localhost:8000`

## Variables de entorno

Puedes copiar `.env.example` como base. Las variables más relevantes son:

- `FRONTEND_ORIGIN`: origen permitido por CORS en el backend.
- `PUBLIC_API_BASE_URL`: URL del backend usada por el frontend.

## Notas

- El backend usa spaCy para el análisis lingüístico.
- Si `es_core_news_lg` no está instalado, el servicio cae a un modelo mínimo para no bloquear el arranque, pero para probar el flujo real conviene instalar el modelo grande.
- El proyecto está pensado para una sola palabra por consulta, no para frases completas.

## Desarrollo

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
pnpm install
pnpm run dev
```

## Tests

```bash
cd backend
pytest
```

## Credits

This project is built with:

- **[FastAPI](https://fastapi.tiangolo.com/)** — Modern, fast web framework for building APIs with Python 3.7+.
- **[spaCy](https://spacy.io/)** — Industrial-strength Natural Language Processing library, with Spanish language models (`es_core_news_lg`).
- **[Astro](https://astro.build/)** — The web framework for content-driven sites, static generation, and hybrid rendering.
- **[Tailwind CSS](https://tailwindcss.com/)** — Utility-first CSS framework for rapidly building custom designs.

Special thanks to the open-source communities behind these projects.

IA:

- [Perplexity](https://www.perplexity.ai/search/3ba0a6b7-6f1c-4500-9a51-92c95a840791)
- [Gemini](https://gemini.google.com/app/e03863e1b748c4d3)