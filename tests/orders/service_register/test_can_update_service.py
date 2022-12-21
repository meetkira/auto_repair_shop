import pytest


@pytest.mark.django_db
def test_can_update_service(client, service_register, create_user_token):
    data = {
        "price": 1300,
        "name": "update_name",
    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.put(
        f"/orders/services/service/{service_register.id}/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["name"] == data["name"]
    assert response.data["price"] == data["price"]
