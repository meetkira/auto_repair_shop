import pytest

from cars.serializers import CarSerializer


@pytest.mark.django_db
def test_can_get_car(client, car, get_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_user_token}'}

    response = client.get(
        f"/cars/car/{car.id}/",
        **bearer
    )
    assert response.status_code == 200
    assert response.data == CarSerializer(car).data
