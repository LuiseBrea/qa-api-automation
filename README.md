# QA API Automation — JSONPlaceholder

Suite de pruebas automatizadas de API construida con **Python + pytest + requests**,
contra la API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com/).

Este es mi primer proyecto de automatización, parte de mi tránsito de QA manual/API
(Postman, validación de datos) hacia QA de automatización. Las pruebas cubren los
mismos criterios que antes validaba a mano en Postman: código de estado, estructura
de la respuesta, tipos de dato y reglas de negocio básicas — pero ahora automatizadas,
versionadas y ejecutables en un pipeline de CI/CD.

## Qué se valida

**`tests/test_posts.py`**
- `GET /posts` devuelve 200 y una lista con el tamaño esperado
- `GET /posts/{id}` devuelve 200 con el esquema correcto (userId, id, title, body)
- `GET /posts/{id}` con un id inexistente devuelve 404
- `POST /posts` crea un recurso y devuelve 201 con los campos enviados
- `PUT /posts/{id}` actualiza y devuelve 200 con los campos actualizados
- `PATCH /posts/{id}` hace una actualización parcial y devuelve 200
- `DELETE /posts/{id}` devuelve 200
- `GET /posts?userId=1` filtra correctamente — todos los resultados pertenecen a ese usuario

**`tests/test_users.py`**
- `GET /users` devuelve 200 con 10 usuarios
- `GET /users/{id}` devuelve 200 con el esquema completo (name, email, address, company)
- Cada email de usuario tiene formato válido (contiene "@" y ".")

> Nota: JSONPlaceholder es una API simulada — los `POST`, `PUT`, `PATCH` y `DELETE`
> responden como si el cambio se guardara, pero no persisten datos reales. Las
> pruebas validan el **contrato de la API** (status code, estructura, eco de los
> datos enviados), no persistencia real. Esto es intencional y así se documenta en
> los propios tests.

## Stack

- Python 3.11+
- pytest
- requests
- pytest-html (reportes)
- GitHub Actions (CI)

## Cómo correrlo localmente

```bash
git clone <tu-repo>
cd qa-api-automation
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

pytest -v                                  # correr todo
pytest -v --html=report.html --self-contained-html   # con reporte HTML
```

## CI/CD

El workflow en `.github/workflows/tests.yml` ejecuta toda la suite automáticamente
en cada push y pull request, y publica el reporte HTML como artefacto descargable.

## Próximos pasos (roadmap personal)

- [ ] Semana 2: automatización de UI con Playwright sobre saucedemo.com
- [ ] Semana 3: Page Object Model + combinar creación de datos por API con verificación en UI
- [ ] Semana 4: reportes con Allure
- [ ] Semana 5: fundamentos de Selenium

---
Proyecto de práctica personal — Luis Enrique Brea · [LinkedIn](https://linkedin.com/in/luis-brea-51b75322b)
