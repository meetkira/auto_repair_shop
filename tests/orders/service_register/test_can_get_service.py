import pytest

from orders.serializers import ServiceSerializer


@pytest.mark.django_db
def test_can_get_service(client, service_register, create_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.get(
        f"/orders/services/service/{service_register.id}/",
        **bearer,
    )
    assert response.status_code == 200
    assert response.data == ServiceSerializer(service_register).data
