import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def base_url():
    """URL base de la API bajo prueba. Centralizada aquí para poder
    apuntar la suite a otro entorno (staging, mock local, etc.) cambiando
    una sola línea."""
    return BASE_URL


@pytest.fixture(scope="session")
def api_session():
    """Sesión de requests reutilizada en toda la suite: evita reabrir
    una conexión TCP por cada request y permite fijar headers comunes."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json; charset=UTF-8"})
    yield session
    session.close()
