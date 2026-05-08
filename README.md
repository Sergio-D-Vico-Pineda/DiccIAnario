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

También puedes probar la API directamente con `curl` o PowerShell:

```powershell
Invoke-RestMethod `
	-Method Post `
	-Uri http://localhost:8000/api/validate `
	-ContentType "application/json" `
	-Body '{"term":"corriendo"}'
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