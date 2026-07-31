# Base de Datos

## Motor principal

- PostgreSQL

## Motor para pruebas

- SQLite en memoria

---

## ORM

SQLAlchemy ORM

---

## Migraciones

Alembic

Comandos principales:

```bash
alembic revision --autogenerate -m "mensaje"
```

```bash
alembic upgrade head
```

```bash
alembic downgrade -1
```

---

## Entidades implementadas

- User
- Project
- ProjectMember
- Board
- Task
- Comment
- Attachment
- Notification
- ActivityLog

---

## Relaciones

User

↓

Project

↓

Board

↓

Task

↓

Comment

↓

Attachment

Además:

- Project → ProjectMember
- Project → Notification
- Project → ActivityLog

---

## Convenciones

Todas las tablas utilizan:

- id
- created_at
- updated_at (cuando aplica)

Las claves foráneas mantienen integridad referencial.