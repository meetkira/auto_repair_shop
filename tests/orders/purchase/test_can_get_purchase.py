import pytest

from orders.serializers import PurchaseSerializer


@pytest.mark.django_db
def test_can_get_purchase(client, spare_part_purchase, create_user_token):

    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.get(
        f"/orders/purchases/purchase/{spare_part_purchase.purchase.id}/",
        **bearer,
    )
    assert response.status_code == 200
    assert response.data == PurchaseSerializer(spare_part_purchase.purchase).data
