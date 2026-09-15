"""Pruebas del recurso /users: esquema, tipos de dato y reglas de formato básicas."""
import pytest

REQUIRED_USER_FIELDS = {"id", "name", "username", "email", "address", "phone", "company"}


@pytest.mark.smoke
def test_get_all_users_returns_200_and_ten_users(base_url, api_session):
    response = api_session.get(f"{base_url}/users")

    assert response.status_code == 200
    users = response.json()
    assert len(users) == 10


@pytest.mark.smoke
def test_get_single_user_has_expected_schema(base_url, api_session):
    response = api_session.get(f"{base_url}/users/1")

    assert response.status_code == 200
    user = response.json()
    assert REQUIRED_USER_FIELDS.issubset(user.keys())
    assert "street" in user["address"]
    assert "city" in user["address"]


@pytest.mark.regression
def test_every_user_has_a_valid_looking_email(base_url, api_session):
    response = api_session.get(f"{base_url}/users")
    users = response.json()

    for user in users:
        email = user["email"]
        assert "@" in email, f"Email sin '@': {email} (usuario id={user['id']})"
        domain = email.split("@")[1]
        assert "." in domain, f"Dominio sin punto: {email} (usuario id={user['id']})"


def test_get_nonexistent_user_returns_404(base_url, api_session):
    response = api_session.get(f"{base_url}/users/9999")

    assert response.status_code == 404
