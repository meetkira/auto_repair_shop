import pytest


@pytest.mark.django_db
def test_delete_individual_user(client, individual_user, get_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_user_token}'}

    response = client.delete(
        "/users/individual/",
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 204


@pytest.mark.django_db
def test_can_delete_entity_user(client, entity_user, get_entity_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_entity_user_token}'}

    response = client.delete(
        "/users/entity/",
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 204
