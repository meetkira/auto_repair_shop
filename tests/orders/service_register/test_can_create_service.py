import pytest


@pytest.mark.django_db
def test_can_create_service(client, create_user_token):
    data = {
        "price": 1000,
        "name": "test_service",
    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.post(
        "/orders/services/create/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data["name"] == data["name"]
    assert response.data["price"] == data["price"]
