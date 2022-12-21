import pytest


@pytest.mark.django_db
def test_can_update_purchase(client, spare_part_purchase, create_user_token):
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.delete(
        f"/orders/purchases/purchase/{spare_part_purchase.purchase.id}/",
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 204
