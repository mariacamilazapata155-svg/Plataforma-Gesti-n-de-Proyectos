# Autenticación

La autenticación utiliza JWT (JSON Web Token).

---

## Flujo

Usuario

↓

Login

↓

Validación de contraseña

↓

Generación de JWT

↓

Cliente almacena el token

↓

Cada petición incluye:

Authorization: Bearer <token>

---

## Componentes

- Hash de contraseñas mediante Passlib (bcrypt)
- JWT con python-jose
- Dependencias FastAPI

---

## Funciones principales

create_access_token()

verify_password()

hash_password()

get_current_user()

---

## Seguridad

Las contraseñas nunca se almacenan en texto plano.

Todos los tokens poseen fecha de expiración.