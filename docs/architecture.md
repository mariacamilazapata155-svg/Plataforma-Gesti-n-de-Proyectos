# Arquitectura

## Objetivo

La aplicación sigue una arquitectura en capas cuyo propósito es separar responsabilidades, facilitar el mantenimiento y permitir el crecimiento del proyecto sin afectar módulos existentes.

---

## Arquitectura general

```text
Cliente
    │
    ▼
Routers (API REST)
    │
    ▼
Services (Lógica de negocio)
    │
    ▼
CRUD (Acceso a datos)
    │
    ▼
Models (SQLAlchemy)
    │
    ▼
PostgreSQL
```

---

## Capas

### Routers

Responsables de:

- Definir endpoints.
- Validar solicitudes HTTP.
- Gestionar códigos de respuesta.
- Invocar la capa Service.

No contienen lógica de negocio.

---

### Services

Implementan toda la lógica del sistema.

Responsabilidades:

- Validaciones complejas.
- Reglas de negocio.
- Gestión de permisos.
- Registro de actividad.
- Envío de notificaciones.

---

### CRUD

Únicamente realizan operaciones sobre la base de datos.

No contienen reglas de negocio.

---

### Models

Representan las tablas mediante SQLAlchemy ORM.

Cada modelo define:

- Columnas
- Relaciones
- Restricciones

---

### Schemas

Definen:

- Validación de entrada
- Validación de salida
- Serialización
- Deserialización

Utilizan Pydantic.

---

## Ventajas

- Bajo acoplamiento
- Alta cohesión
- Fácil mantenimiento
- Código reutilizable
- Alta escalabilidad