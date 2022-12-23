import pytest


@pytest.mark.django_db
def test_can_delete_service(client, service_register, create_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.delete(
        f"/orders/services/service/{service_register.id}/",
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 204
