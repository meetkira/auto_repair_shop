import pytest


@pytest.mark.django_db
def test_can_get_car(client, car, get_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_user_token}'}

    response = client.delete(
        f"/cars/car/{car.id}/",
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 204
