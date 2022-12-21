import pytest


@pytest.mark.django_db
def test_can_create_spare_part(client, create_user_token):
    data = {
        "car_model": "123A",
        "car_brand": "BMW",
        "price": 1000,
        "name": "test_spare_part",
        "amount": 120,
    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.post(
        "/orders/spare_parts/create/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data["car_model"] == data["car_model"]
    assert response.data["price"] == data["price"]
