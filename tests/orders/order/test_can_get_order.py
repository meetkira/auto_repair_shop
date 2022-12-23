import pytest

from orders.serializers import OrderSerializer
from tests.factories import OrderFactory, SparePartOrderFactory


@pytest.mark.django_db
def test_can_get_order(client, service_register, create_user_token):

    order = OrderFactory.create(services=(service_register, ))
    SparePartOrderFactory.create(order=order)

    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.get(
        f"/orders/order/{order.id}/",
        **bearer,
    )
    assert response.status_code == 200
    assert response.data == OrderSerializer(order).data
