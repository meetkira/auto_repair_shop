import pytest


@pytest.mark.django_db
def test_can_create_individual_user(client):
    data = {
        "first_name": "test first name",
        "last_name": "test last name",
        "email": "testemail@mail.ru",
        "password": "testpassword12345",
        "is_worker": False,
        "passport": "1234 567891"
    }

    response = client.post(
        "/users/signup/individual/",
        data=data,
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data["first_name"] == "test first name"
    assert response.data["last_name"] == "test last name"


@pytest.mark.django_db
def test_can_create_entity_user(client):
    data = {
        "email": "testemail@mail.ru",
        "password": "testpassword12345",
        "title": "test title",
        "requisites": "1234567890"
    }

    response = client.post(
        "/users/signup/entity/",
        data=data,
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data["title"] == "test title"
    assert response.data["requisites"] == "1234567890"
