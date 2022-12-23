import pytest

from tests.factories import OrderFactory, SparePartOrderFactory


@pytest.mark.django_db
def test_can_update_order(client, service_register, create_user_token):
    order = OrderFactory.create(services=(service_register,))
    SparePartOrderFactory.create(order=order)
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.delete(
        f"/orders/order/{order.id}/",
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 204
