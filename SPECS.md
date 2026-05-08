# SPECS.md

## Proyecto
**Validador Lingüístico Inteligente (NLP + RAE)**

Aplicación web para validar palabras del español mediante análisis lingüístico, clasificación gramatical y verificación de enlace oficial al Diccionario de la Lengua Española (DLE/RAE).

## 1. Propósito
Construir una aplicación web rápida, mantenible y orientada a portfolio que permita:

- Determinar si una palabra introducida por el usuario puede considerarse válida dentro del español estándar de consulta.
- Analizar su forma lingüística usando NLP (Natural Language Processing), con foco en lematización, rasgos morfológicos y categoría gramatical.
- Generar y comprobar un enlace oficial de consulta en la RAE antes de presentarlo al usuario.
- Separar inteligentemente frontend, backend y motor lingüístico.

## 2. Objetivos del producto

### Objetivo principal
Ofrecer una validación “inteligente” de palabras en español que no dependa únicamente de una coincidencia literal, sino que use análisis morfológico para reconocer variantes flexionadas como participios, conjugaciones o plurales.

### Objetivos secundarios
- Mostrar el lema detectado de la palabra.
- Indicar la categoría gramatical principal, por ejemplo: sustantivo, verbo, adjetivo, adverbio, determinantes, pronombre, preposición, conjunción e interjección.
- Informar si existe una URL verificable en el DLE para la palabra o para su lema.
- Entregar una UX muy rápida, simple y clara.

## 3. Alcance funcional

### Incluye
- Entrada de una sola palabra.
- Normalización del input.
- Análisis NLP en español con spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)).
- Extracción de lema, POS y rasgos morfológicos.
- Heurística de validez lingüística.
- Construcción de URL oficial del DLE.
- Verificación HTTP de la URL antes de mostrarla.
- Respuesta JSON desde API.
- Interfaz web en Astro + Tailwind CSS.
- Estado visual de éxito, advertencia o no encontrado.
- Manejo de errores y timeouts.

### Evitar / No incluirá nunca
- Búsqueda por frases largas u oraciones completas.
- Corrección ortográfica avanzada tipo autocorrector.
- Scraping intensivo o redistribución de contenido de la RAE.

### No incluye en la v1
- Definiciones del diccionario embebidas en la app.
- Historial persistente de consultas.
- Cuentas de usuario.
- Entrenamiento de modelos propios.

## 4. Usuarios objetivo
- Usuarios generales que quieren verificar si una palabra existe o cómo debe consultarse.
- Estudiantes o desarrolladores interesados en lingüística computacional en español.
- Verificar que la palabra introducida existe en el lenguaje español.

## 5. Propuesta de valor
A diferencia de un validador literal, el sistema puede interpretar formas flexionadas y devolver información lingüística útil junto con un enlace oficial verificable a la RAE. FastAPI está diseñado para alto rendimiento y soporta rutas asíncronas, lo que encaja bien con una API ligera de validación. El modelo `es_core_news_lg` de spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)) para español incluye, entre otros componentes, `morphologizer`, `parser`, `attribute_ruler` y `lemmatizer`, por lo que cubre las piezas necesarias para lematización y análisis gramatical. La RAE documenta rutas directas del tipo `https://dle.rae.es/palabra`, útiles para enlazar consultas oficiales.

## 6. Arquitectura

### Frontend
**Astro + Tailwind CSS**

Responsabilidades:
- Renderizar la interfaz.
- Gestionar formulario y estados visuales.
- Consumir el endpoint de validación.
- Mostrar resultado, lema, categoría y enlace RAE.

Principios:
- Zero JS por defecto, activando solo el mínimo necesario para la interacción.
- Carga rápida.
- Diseño minimalista y responsive.

### Backend
**FastAPI (Python)**

Responsabilidades:
- Exponer la API REST.
- Validar y sanear el input.
- Ejecutar el análisis lingüístico.
- Resolver estrategia de validación.
- Comprobar existencia del enlace en la RAE.
- Devolver respuesta estructurada y cacheable.

FastAPI ofrece soporte claro para `async/await`, útil cuando conviven procesamiento interno y operaciones I/O como verificación HTTP.

### Motor NLP
**spaCy + `es_core_news_lg`** (alternativa: [stanza](https://stanfordnlp.github.io/stanza/))

Responsabilidades:
- Tokenizar el término.
- Lematizar.
- Detectar POS.
- Leer rasgos morfológicos.
- Proveer una base lingüística para decidir si una forma flexionada puede ser aceptada.

El modelo `es_core_news_lg` para español está optimizado para CPU e incluye lematizador y analizador morfológico dentro de su pipeline.

### Integración externa
**HTTPX + BeautifulSoup**

Responsabilidades:
- Probar la URL generada del DLE.
- Detectar si hay página válida, redirección útil o ausencia de resultado.
- Extraer señales mínimas de confirmación sin replicar contenido del diccionario.

## 7. Flujo funcional
1. El usuario escribe una palabra, por ejemplo `corriendo`.
2. El frontend normaliza y envía la consulta al backend.
3. El backend procesa el input.
4. spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)) analiza el término y devuelve lema, POS y morfología.
5. El motor de reglas evalúa si la palabra es aceptable como forma lingüística.
6. El backend construye una o varias URLs candidatas del DLE, por ejemplo con la forma original y con el lema. La ayuda oficial de la RAE muestra ejemplos de consulta directa como `https://dle.rae.es/universo` y `https://dle.rae.es/duermevela`.
7. El backend verifica la disponibilidad real del recurso.
8. La API responde con estado, explicación, datos lingüísticos y enlace final.
9. El frontend presenta el resultado con feedback visual claro.

## 8. Reglas de negocio

### Entrada aceptada
- Solo una palabra.
- Longitud mínima: 3 carácter.
- Longitud máxima sugerida: 25 caracteres.
- Se aceptan tildes, eñes y diéresis.
- Se recortan espacios laterales.

### Normalización
- Trim de espacios.
- Normalización Unicode NFC.
- Conversión a minúsculas para validación interna, manteniendo versión original para UI.
- Rechazo de inputs con números o símbolos no permitidos (guion).

### Criterios de validez
La respuesta final no debe basarse en una sola señal. Debe combinar:

- **Señal lingüística**: spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)) reconoce el token, lema y POS plausibles.
- **Señal morfológica**: la forma parece una flexión válida del lema.
- **Señal externa**: existe consulta utilizable en el DLE para forma original o lema.
- **Heurística de confianza**: clasificar como `valid`, `likely_valid`, `unknown`, `invalid`.

### Casos esperados
- `correr` → válido, verbo, enlace directo si existe.
- `corriendo` → válido, se enlaza al lema `correr`.
- `casas` → válido por plural de `casa`; enlazar al lema en sigular.
- `asdfgh` → inválido.

## 9. Diseño de API

### Endpoint principal
`POST /api/validate`

### Request JSON
```json
{
  "term": "corriendo"
}
```

### Response JSON esperada
```json
{
  "input": "corriendo",
  "normalized": "corriendo",
  "is_valid": true,
  "confidence": "high",
  "classification": "verbo",
  "pos": "VERB",
  "lemma": "correr",
  "rae": {
    "checked_term": "correr",
    "url": "https://dle.rae.es/correr",
    "exists": true,
    "status_code": 200
  },
  "warnings": []
}
```

### Códigos de respuesta
- `200 OK`: consulta procesada.
- `400 Bad Request`: input vacío o inválido.
- `422 Unprocessable Entity`: payload incorrecto.
- `429 Too Many Requests`: limitación básica opcional.
- `500 Internal Server Error`: error inesperado.
- `503 Service Unavailable`: fallo temporal al comprobar RAE.

## 10. Contrato interno del motor lingüístico

### Módulos sugeridos
```text
app/
  main.py
  api/
    routes_validate.py
  core/
    config.py
    logging.py
  services/
    nlp_service.py
    validation_service.py
    rae_service.py
  schemas/
    request.py
    response.py
  utils/
    text_normalizer.py
    pos_mapper.py
```

### Responsabilidades
- `nlp_service.py`: carga singleton del modelo spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)) y parsing.
- `validation_service.py`: reglas de decisión y scoring.
- `rae_service.py`: construcción y verificación de URLs DLE.
- `pos_mapper.py`: traducción de etiquetas `VERB`, `NOUN`, `ADJ` a etiquetas legibles en español.

## 11. Algoritmo de validación

### Pipeline propuesto
1. Validar formato del input.
2. Normalizar término.
3. Ejecutar `nlp(term)`.
4. Verificar que el análisis produzca un único token principal o una estrategia controlada para multi-token.
5. Extraer:
   - `token.text`
   - `token.lemma_`
   - `token.pos_`
   - `token.morph`
6. Calcular una puntuación heurística.
7. Generar URLs candidatas:
   - `https://dle.rae.es/{input_normalized}`
   - `https://dle.rae.es/{lemma}`
8. Comprobar la mejor URL disponible.
9. Construir explicación legible.
10. Devolver resultado final.

### Heurística inicial sugerida
```text
score = 0
+ 0.35 si hay lema no vacío
+ 0.20 si POS pertenece a categorías léxicas válidas
+ 0.20 si los rasgos morfológicos son coherentes
+ 0.25 si existe URL verificable en DLE
```

### Umbrales
- `>= 0.80` → `valid`
- `0.60 - 0.79` → `likely_valid`
- `0.35 - 0.59` → `unknown`
- `< 0.35` → `invalid`

## 12. Integración con RAE

### Estrategia de enlace
La RAE ofrece ejemplos de consulta directa por ruta, como `https://dle.rae.es/universo`, lo que permite construir enlaces limpios por palabra.

### Reglas de comprobación
- Intentar primero la forma original normalizada.
- Si falla, intentar el lema.
- Seguir redirecciones controladas.
- Considerar timeout corto, por ejemplo 2-4 s.
- No almacenar ni redistribuir definiciones completas.
- Solo exponer URL y evidencia mínima de existencia.

### Consideraciones legales y éticas
- No scrapear, solo comprobar que URL existe.
- Respetar robots, límites y uso razonable.

## 13. Requisitos no funcionales

### Rendimiento
- Tiempo objetivo API sin consulta externa: < 150 ms en local tras calentar modelo.
- Tiempo objetivo con verificación RAE: < 800 ms promedio, sujeto a red.
- Reutilización del modelo spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)) en memoria.
- Posible caché LRU/TTL para consultas repetidas.

### Escalabilidad
- Backend stateless.
- Despliegue en contenedor Docker.
- Posibilidad futura de cola para verificaciones lentas.

### Mantenibilidad
- Arquitectura por capas.
- Tipado con Pydantic.
- Servicios desacoplados.
- Pruebas unitarias y de integración.

### Observabilidad
- Logs estructurados.
- Métricas básicas: latencia, ratio de acierto, errores RAE.
- Trazas de timeouts y fallos externos.

### Seguridad
- Sanitización de entrada.
- Rate limiting opcional.
- CORS restringido por entorno.
- Timeouts de red y user-agent definido.

## 14. Frontend UX/UI

### Pantalla principal
- Hero simple con propuesta de valor.
- Input central de búsqueda.
- Botón “Validar”.
- Resultado en tarjeta.

### Estados UI
- Idle.
- Loading.
- Válido.
- Probablemente válido.
- No encontrado.
- Error temporal.

### Resultado visible
- Término consultado.
- Estado de validez.
- Lema detectado.
- Categoría gramatical.
- Rasgos relevantes.
- Enlace oficial RAE.
- Mensaje interpretativo breve.

### Criterios de diseño
- Minimalista.
- Mobile-first.
- Accesible por teclado.
- Sin sobrecargar la interfaz con tecnicismos.

## 15. Stack técnico definitivo

| Capa | Tecnología | Motivo |
|---|---|---|
| Frontend | Astro | Sitio rápido, contenido estático + islas ligeras |
| UI | Tailwind CSS | Productividad y consistencia visual |
| Cliente HTTP | Fetch API | Suficiente para una interacción simple |
| Backend | FastAPI | API moderna, tipada y de alto rendimiento |
| NLP | spaCy `es_core_news_lg` (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)) | Lematización, morfología y sintaxis en español |
| HTTP externo | HTTPX | Cliente moderno con buen soporte async |
| Parsing HTML | BeautifulSoup | Extracción mínima y robusta |
| Validación de datos | Pydantic | Contratos claros request/response |
| Tests | Pytest | Base estándar para backend Python |
| Deploy | Docker + plataforma cloud | Portabilidad y despliegue reproducible |

## 16. Estructura del repositorio
```text
linguistic-validator/
├─ backend/
│  ├─ app/
│  ├─ tests/
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ src/
│  ├─ public/
│  ├─ astro.config.mjs
│  └─ package.json
├─ docs/
│  └─ architecture.md
├─ .env.example
├─ docker-compose.yml
├─ README.md
└─ SPECS.md
```

## 17. Variables de entorno
```env
APP_ENV=development
API_PORT=8000
FRONTEND_ORIGIN=http://localhost:4321
REQUEST_TIMEOUT_RAE=3.0
USER_AGENT=linguistic-validator/1.0
ENABLE_RAE_CHECK=true
CACHE_TTL_SECONDS=3600
```

## 18. Testing

### Unit tests
- Normalización de texto.
- Mapeo POS.
- Reglas heurísticas.
- Construcción de URL RAE.

### Integration tests
- `POST /api/validate` con casos válidos e inválidos.
- Fallback de término original a lema.
- Manejo de timeout externo.

### Casos de prueba mínimos
- `correr`
- `corriendo`
- `casa`
- `casas`
- `bonito`
- `rápidamente`
- `asdfgh`
- `1234`
- cadena vacía

## 19. Roadmap por fases

### Fase 1 — MVP
- API FastAPI funcional.
- Carga de spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)).
- Endpoint de validación.
- UI básica en Astro.
- Verificación de enlace RAE.

### Fase 2 — Calidad
- Caché TTL.
- Mejoras de heurística.
- Tests amplios.
- Manejo fino de errores.
- Observabilidad mínima.

### Fase 3 — Mejora de producto
- Historial local de consultas.
- Sugerencias cuando no exista coincidencia.
- Sinónimos o variantes cercanas.
- Batch validation opcional.

## 20. Criterios de aceptación
- El usuario puede introducir una palabra y recibir respuesta en menos de 1 segundo en condiciones normales.
- La respuesta incluye lema y categoría gramatical cuando el análisis lo permite.
- La app intenta enlazar a la forma exacta y, si no existe, al lema.
- El sistema no rompe cuando la RAE no responde; devuelve estado degradado controlado.
- La arquitectura separa claramente UI, API y servicios lingüísticos.
- El código resulta apto para portfolio técnico y fácil de desplegar.

## 21. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| El modelo spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)) acepta formas raras o ambiguas | Medio | Añadir scoring y reglas adicionales |
| La palabra existe lingüísticamente pero no como entrada directa | Alto | Fallback automático al lema |
| Latencia externa alta | Medio | Timeout corto + caché + respuesta degradada |
| Ambigüedad gramatical | Medio | Mostrar clasificación principal y advertencias |

## 22. Definición de terminado
El proyecto se considera terminado para v1 cuando exista una web funcional desplegable con frontend en Astro, API en FastAPI y análisis con spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)), capaz de recibir una palabra, inferir lema y POS, verificar un enlace útil del DLE y mostrar un resultado claro al usuario. La base técnica propuesta está alineada con capacidades documentadas de FastAPI para trabajo asíncrono y con el pipeline del modelo `es_core_news_lg` de spaCy (alternativa: [stanza](https://stanfordnlp.github.io/stanza/)) para español.