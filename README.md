# Plataforma Gestión de Proyectos

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)
![Status](https://img.shields.io/badge/Status-Development-orange)

Backend desarrollado con FastAPI para la gestión colaborativa de proyectos, tableros Kanban, tareas y equipos de trabajo.

El proyecto sigue una arquitectura en capas (Routers → Services → CRUD → Models) con énfasis en mantenibilidad, escalabilidad y buenas prácticas de ingeniería de software.

<p align="center">
    <img src="docs/images/architecture.png" width="200">
</p>

Más información en:

→ [Arquitectura del sistema](docs/architecture.md)


---

# Características

- API REST con FastAPI
- Arquitectura en capas
- Autenticación mediante JWT
- Autorización basada en roles (RBAC)
- SQLAlchemy ORM
- Alembic para migraciones
- PostgreSQL
- Pytest para pruebas automatizadas
- Documentación automática con Swagger y ReDoc

---

# Tecnologías

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Passlib
- JWT
- Pytest
- SQLite (entorno de pruebas)

---

# Funcionalidades implementadas

- Gestión de usuarios
- Autenticación JWT
- Gestión de proyectos
- Gestión de miembros de proyectos
- Gestión de tableros Kanban
- Gestión de tareas
- Comentarios
- Archivos adjuntos
- Notificaciones
- Historial de actividades
- Sistema de permisos por roles

---

# Instalación

Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/plataforma-gestion-proyectos.git
```

Entrar al proyecto

```bash
cd backend
```

Crear el entorno virtual

```bash
python -m venv .venv
```

Activarlo

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Variables de entorno

Crear un archivo `.env`

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/project_db

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# Ejecutar el proyecto

Aplicar migraciones

```bash
alembic upgrade head
```

Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Ejecutar las pruebas

Todas las pruebas

```bash
python -m pytest
```

Modo detallado

```bash
python -m pytest -v
```

Cobertura

```bash
pytest --cov=app
```

---

# Estado actual

El proyecto se encuentra en desarrollo activo.

Actualmente incluye:

- Arquitectura principal completamente implementada.
- Autenticación y autorización.
- Gestión de proyectos.
- Gestión de miembros.
- Gestión de tableros.
- Gestión de tareas.
- Comentarios.
- Archivos adjuntos.
- Notificaciones.
- Historial de actividades.
- Suite inicial de pruebas automatizadas.

---

# Documentación

La documentación técnica del proyecto se encuentra organizada en la carpeta `docs`.

| Documento | Descripción |
|------------|-------------|
| [Arquitectura](docs/architecture.md) | Arquitectura general del backend |
| [Estructura del proyecto](docs/project_structure.md) | Organización del código fuente |
| [Base de datos](docs/database.md) | Modelo de datos y relaciones |
| [Autenticación](docs/authentication.md) | JWT y flujo de autenticación |
| [Autorización](docs/authorization.md) | Control de acceso |
| [Permisos](docs/permissions.md) | Roles del sistema |
| [API](docs/api.md) | Endpoints principales |
| [Pruebas](docs/testing.md) | Estrategia de testing |
| [Roadmap](docs/roadmap.md) | Funcionalidades futuras |

---

# Versiones

El historial completo de cambios puede consultarse en:

→ [CHANGELOG.md](CHANGELOG.md)

El proyecto sigue Versionado Semántico (Semantic Versioning).

Versión actual:

**v0.1.0**

---

# Documentación adicional

- [Guía de contribución](CONTRIBUTING.md)
- [Código de conducta](CODE_OF_CONDUCT.md)
- [Política de seguridad](SECURITY.md)
- [Historial de cambios](CHANGELOG.md)
- [Licencia MIT](LICENSE)

---

# Licencia

Este proyecto se distribuye bajo la licencia MIT.

Consulta el archivo `LICENSE` para más información.

---

# Autor

María Camila

Ingeniera de Software

Proyecto desarrollado con fines de aprendizaje y fortalecimiento profesional, aplicando buenas prácticas de desarrollo backend con FastAPI, SQLAlchemy y PostgreSQL.