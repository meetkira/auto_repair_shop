import pytest


@pytest.mark.django_db
def test_can_create_car(client, individual_user, get_user_token):
    data = {
        "user": individual_user.id,
        "model": "123A",
        "brand": "BMW",
        "number": "А123КМ45",
        "color": "black"
    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_user_token}'}

    response = client.post(
        "/cars/create/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data["model"] == data["model"]
    assert response.data["brand"] == data["brand"]
