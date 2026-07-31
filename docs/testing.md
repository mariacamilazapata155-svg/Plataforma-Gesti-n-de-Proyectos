# Testing

El proyecto utiliza Pytest para validar el comportamiento de la API.

---

## Objetivos

- Detectar regresiones
- Validar permisos
- Verificar reglas de negocio
- Garantizar estabilidad

---

## Base de datos

Las pruebas utilizan:

SQLite en memoria

Cada prueba crea una base completamente limpia.

---

## Cobertura actual

Se encuentran implementadas pruebas para:

- Autenticación
- Usuarios
- Proyectos
- Miembros
- Tableros
- Tareas
- Comentarios
- Adjuntos
- Notificaciones
- Historial de actividad

---

## Ejecución

```bash
pytest
```

```bash
pytest -v
```

```bash
pytest --cov=app
```