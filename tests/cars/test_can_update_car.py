import pytest


@pytest.mark.django_db
def test_can_update_car(client, car, get_user_token):
    data = {
        "model": "update_model",
        "brand": "update_brand",
        "number": car.number,
        "color": car.color,
    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_user_token}'}

    response = client.put(
        f"/cars/car/{car.id}/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["model"] == data["model"]
