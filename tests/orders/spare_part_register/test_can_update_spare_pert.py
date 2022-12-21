import pytest


@pytest.mark.django_db
def test_can_update_spare_part(client, spare_part_register, create_user_token):
    data = {
        "car_model": "update_model",
        "car_brand": "update_brand",
        "price": spare_part_register.price,
        "name": "update_name",
        "amount": 120,
    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.put(
        f"/orders/spare_parts/spare_part/{spare_part_register.id}/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["car_model"] == data["car_model"]
    assert response.data["price"] == data["price"]
