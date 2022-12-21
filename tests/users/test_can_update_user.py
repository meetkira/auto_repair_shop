import pytest


@pytest.mark.django_db
def test_update_individual_user(client, individual_user, get_user_token):
    data = {
        "first_name": "update",
        "email": individual_user.email,
    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_user_token}'}

    response = client.put(
        "/users/individual/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["first_name"] == data["first_name"]


@pytest.mark.django_db
def test_can_update_entity_user(client, entity_user, get_entity_user_token):
    data = {
        "title": "update title",
        "email": entity_user.email,
    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_entity_user_token}'}

    response = client.put(
        "/users/entity/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["title"] == data["title"]
