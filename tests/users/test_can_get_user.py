import pytest

from users.serializers import IndividualUserSerializer, EntityUserSerializer


@pytest.mark.django_db
def test_can_get_individual_user(client, individual_user, get_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_user_token}'}

    response = client.get(
        "/users/individual/",
        **bearer
    )
    assert response.status_code == 200
    assert response.data == IndividualUserSerializer(individual_user).data


@pytest.mark.django_db
def test_can_get_entity_user(client, entity_user, get_entity_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {get_entity_user_token}'}

    response = client.get(
        "/users/entity/",
        **bearer
    )
    assert response.status_code == 200
    assert response.data == EntityUserSerializer(entity_user).data
