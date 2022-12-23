import pytest

from users.models import IndividualUser


@pytest.fixture
@pytest.mark.django_db
def create_user_token(client):
    email = "testuser@ya.ru"
    password = "testuserpassword"

    IndividualUser.objects.create_user(email=email, password=password, is_worker=True, first_name="test",
                                       last_name="test", passport="0123 456789")

    response = client.post(
        "/users/token/",
        {"email": email, "password": password},
        content_type='application/json',
    )

    return response.data["access"]


@pytest.fixture
@pytest.mark.django_db
def get_user_token(client):
    email = "testindividualuser@ya.ru"
    password = "testuserpassword"

    response = client.post(
        "/users/token/",
        {"email": email, "password": password},
        content_type='application/json',
    )

    return response.data["access"]


@pytest.fixture
@pytest.mark.django_db
def get_entity_user_token(client):
    email = "testentityuser@ya.ru"
    password = "testuserpassword"

    response = client.post(
        "/users/token/",
        {"email": email, "password": password},
        content_type='application/json',
    )

    return response.data["access"]
