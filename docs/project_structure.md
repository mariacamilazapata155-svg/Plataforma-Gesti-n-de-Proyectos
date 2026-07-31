# Estructura del Proyecto

```text
backend/
│
├── alembic/
├── app/
│
│   ├── core/
│   ├── crud/
│   ├── db/
│   ├── enums/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│
├── docs/
├── tests/
├── uploads/
├── requirements.txt
└── README.md
```

---

## Descripción

core/

Configuración, seguridad y dependencias.

crud/

Acceso a datos.

services/

Reglas de negocio.

routers/

Endpoints REST.

models/

Modelos SQLAlchemy.

schemas/

Validación mediante Pydantic.

tests/

Pruebas automatizadas.

docs/

Documentación técnica.