# Guía de Contribución

Gracias por tu interés en contribuir a este proyecto.

El objetivo de este repositorio es construir un backend profesional utilizando FastAPI siguiendo buenas prácticas de arquitectura, desarrollo y pruebas automatizadas.

## Requisitos

Antes de comenzar asegúrate de tener instalado:

* Python 3.12 o superior
* PostgreSQL
* Git
* Entorno virtual (venv)

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración inicial

Clona el repositorio.

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd backend
```

Crea un entorno virtual.

```bash
python -m venv .venv
```

Actívalo.

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Instala las dependencias.

```bash
pip install -r requirements.txt
```

---

## 2. Formato del código

```md
## Formato del código

Antes de realizar un Pull Request se recomienda ejecutar:

```bash
black .
isort .
flake8
```

En futuras versiones estas validaciones serán ejecutadas automáticamente mediante GitHub Actions.

---

## 3. Convención para nombres de ramas

Actualmente tienes:

```
text
feature/
fix/
refactor/
test/
docs/
hotfix/
release/
```

---

## Convenciones del proyecto

Se utilizan las siguientes convenciones:

- snake_case para funciones y variables.
- PascalCase para clases.
- UPPER_CASE para constantes.
- Tipado en todas las funciones nuevas.
- Docstrings para funciones públicas.

## Flujo de trabajo

1. Crear una nueva rama.

```bash
git checkout -b feature/nombre-funcionalidad
```

2. Realizar los cambios.

3. Ejecutar todas las pruebas.

```bash
pytest
```

4. Verificar que no existan errores de linting (cuando el proyecto incorpore Ruff o Black).

5. Crear un commit descriptivo.

Ejemplos:

```text
feat: add attachment upload endpoint

fix: correct permission validation

test: add notification tests

docs: update README
```

6. Enviar la rama al repositorio.

```bash
git push origin feature/nombre-funcionalidad
```

7. Abrir un Pull Request.

---

## Estándares de código

El proyecto sigue las siguientes reglas:

* Arquitectura por capas.
* Código tipado.
* Docstrings en funciones públicas.
* Responsabilidad única por función.
* Nombres descriptivos.
* Separación entre Router, Service y CRUD.

---

## Pruebas

Toda nueva funcionalidad debe incluir pruebas automatizadas.

No se aceptarán cambios que rompan la suite de pruebas existente.

Ejecutar:

```bash
pytest -v
```

---

## Convención de ramas

```text
feature/
fix/
refactor/
test/
docs/
```

Ejemplos:

```text
feature/project-members

feature/comments

fix/login

test/attachments

docs/readme
```

---

## Convención de commits

Se recomienda utilizar Conventional Commits.

Ejemplos:

```text
feat:

fix:

refactor:

test:

docs:

style:

chore:
```

---

## Pull Requests

Antes de abrir un Pull Request verifica que:

* Todas las pruebas pasan correctamente.
* No existen archivos temporales.
* No se incluyen credenciales.
* La documentación fue actualizada si era necesario.

Muchas gracias por contribuir.
