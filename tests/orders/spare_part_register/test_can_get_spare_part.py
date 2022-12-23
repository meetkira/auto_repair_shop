import pytest

from orders.serializers import SparePartSerializer

@pytest.mark.django_db
def test_can_get_spare_part(client, spare_part_register, create_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.get(
        f"/orders/spare_parts/spare_part/{spare_part_register.id}/",
        **bearer,
    )
    assert response.status_code == 200
    assert response.data == SparePartSerializer(spare_part_register).data
