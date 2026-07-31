# Autorización

La autorización es independiente de la autenticación.

Una vez autenticado el usuario, el sistema valida si posee permisos para ejecutar la acción solicitada.

---

## Modelo

RBAC

(Role Based Access Control)

---

## Roles

OWNER

ADMIN

MEMBER

VIEWER

---

## Validación

La autorización se implementa mediante:

require_project_role()

Este componente verifica:

- existencia del proyecto
- pertenencia al proyecto
- rol permitido

---

## Ventajas

- Centralización
- Reutilización
- Fácil mantenimiento