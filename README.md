# 🔗 Acortador de URLs · Flask + Docker

![CI](https://github.com/acruzc23-crypto/acortador-urls-flask/actions/workflows/ci.yml/badge.svg)

Servicio web para **acortar enlaces largos**, con alias personalizados y **contador de visitas**. Incluye interfaz web y **API REST**, base de datos **SQLite**, pruebas automatizadas con **pytest** (98 % de cobertura) y despliegue con **Docker**.

## ✨ Funcionalidades

- Acortar URLs con código aleatorio de 6 caracteres o **alias personalizado**
- Redirección `302` y conteo de visitas por enlace
- Reutiliza el código si la URL ya fue acortada
- Validación de URLs y alias (errores claros en web y API)
- Interfaz web con tabla de enlaces recientes
- Endpoint de salud para monitoreo (`/api/salud`)

## 🛠️ Tecnologías

| Área | Herramientas |
|------|--------------|
| Backend | Python 3.12, Flask (Application Factory + Blueprints) |
| Base de datos | SQLite |
| Servidor | Gunicorn |
| Contenedores | Docker, Docker Compose |
| Testing | pytest, pytest-cov |
| CI | GitHub Actions (tests + build y prueba de la imagen Docker) |

## 📡 API REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/enlaces` | Crea un enlace corto. Body: `{"url": "...", "alias": "opcional"}` |
| `GET`  | `/api/enlaces/<codigo>` | Estadísticas del enlace (URL, visitas, fecha) |
| `GET`  | `/<codigo>` | Redirige a la URL original |
| `GET`  | `/api/salud` | Estado del servicio |

Ejemplo:

```bash
curl -X POST http://localhost:8000/api/enlaces \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.unemi.edu.ec", "alias": "unemi"}'
```

```json
{ "codigo": "unemi", "url": "https://www.unemi.edu.ec", "visitas": 0, "url_corta": "http://localhost:8000/unemi" }
```

## 🚀 Cómo ejecutarlo

### Con Docker (recomendado)

```bash
git clone https://github.com/acruzc23-crypto/acortador-urls-flask.git
cd acortador-urls-flask
docker compose up --build
```

Abre http://localhost:8000. Los datos se guardan en un volumen y persisten entre reinicios.

### Sin Docker

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
python wsgi.py
```

## 🧪 Pruebas

```bash
pytest --cov=app
```

11 pruebas que cubren la API, la interfaz web, validaciones, alias duplicados, redirecciones y conteo de visitas. Cada `push` ejecuta las pruebas y además construye y prueba la imagen Docker en GitHub Actions.

## 📁 Estructura

```
app/
├── __init__.py    # create_app(): configuración y registro de blueprints
├── db.py          # conexión y esquema SQLite
├── servicio.py    # lógica de negocio (validar, acortar, resolver)
├── routes.py      # rutas web y API REST
└── templates/     # vistas Jinja2
tests/             # pruebas con pytest
Dockerfile         # imagen con usuario sin privilegios y healthcheck
docker-compose.yml
```

## 📚 Lo que aprendí

- Separar capas: rutas HTTP ↔ lógica de negocio ↔ acceso a datos
- Diseñar una API REST con códigos de estado correctos (201, 302, 400, 404)
- Escribir pruebas con fixtures y base de datos temporal
- Crear imágenes Docker seguras y ligeras, y orquestarlas con Compose
- Integración continua con GitHub Actions

---

👤 **Desarrollado por Alfredo Cruz**, con asistencia de IA (Claude).
Estudiante de Ingeniería en Software — UNEMI, Ecuador.
[GitHub](https://github.com/acruzc23-crypto) · [LinkedIn](https://www.linkedin.com/in/alfredo-cruz-dev)
