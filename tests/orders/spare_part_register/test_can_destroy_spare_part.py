import pytest


@pytest.mark.django_db
def test_can_delete_spare_part(client, spare_part_register, create_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.delete(
        f"/orders/spare_parts/spare_part/{spare_part_register.id}/",
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 204
