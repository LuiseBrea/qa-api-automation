"""
Pruebas del recurso /posts.

JSONPlaceholder es una API simulada: los métodos de escritura (POST, PUT,
PATCH, DELETE) responden como si el cambio se hubiera guardado, pero no
persisten datos reales entre requests. Por eso estas pruebas validan el
CONTRATO de la API (status code, estructura de la respuesta, eco de los
datos enviados) y no la persistencia real — igual que se haría contra un
mock en un pipeline de CI antes de tener ambiente de staging real.
"""
import pytest

REQUIRED_POST_FIELDS = {"userId", "id", "title", "body"}


@pytest.mark.smoke
def test_get_all_posts_returns_200_and_full_list(base_url, api_session):
    response = api_session.get(f"{base_url}/posts")

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == 100  # tamaño fijo y conocido del dataset de prueba


@pytest.mark.smoke
def test_get_single_post_has_expected_schema(base_url, api_session):
    response = api_session.get(f"{base_url}/posts/1")

    assert response.status_code == 200
    post = response.json()
    assert REQUIRED_POST_FIELDS.issubset(post.keys())
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str) and post["title"] != ""


def test_get_nonexistent_post_returns_404(base_url, api_session):
    response = api_session.get(f"{base_url}/posts/99999")

    assert response.status_code == 404


def test_filter_posts_by_user_id_returns_only_that_user(base_url, api_session):
    user_id = 1
    response = api_session.get(f"{base_url}/posts", params={"userId": user_id})

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0
    assert all(post["userId"] == user_id for post in posts)


@pytest.mark.regression
def test_create_post_returns_201_and_echoes_payload(base_url, api_session):
    payload = {
        "title": "Prueba de automatización QA",
        "body": "Contenido de prueba generado por la suite automatizada",
        "userId": 1,
    }

    response = api_session.post(f"{base_url}/posts", json=payload)

    assert response.status_code == 201
    created = response.json()
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]
    assert "id" in created  # la API simulada asigna un id nuevo


@pytest.mark.regression
def test_update_post_with_put_returns_200_and_updated_fields(base_url, api_session):
    payload = {
        "id": 1,
        "title": "Título actualizado por automatización",
        "body": "Cuerpo actualizado",
        "userId": 1,
    }

    response = api_session.put(f"{base_url}/posts/1", json=payload)

    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == payload["title"]
    assert updated["body"] == payload["body"]


@pytest.mark.regression
def test_partial_update_post_with_patch_returns_200(base_url, api_session):
    response = api_session.patch(f"{base_url}/posts/1", json={"title": "Solo cambio el título"})

    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "Solo cambio el título"
    assert updated["id"] == 1  # el resto del recurso no debería alterarse


@pytest.mark.regression
def test_delete_post_returns_200(base_url, api_session):
    response = api_session.delete(f"{base_url}/posts/1")

    assert response.status_code == 200
