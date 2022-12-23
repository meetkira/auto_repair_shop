import pytest

from tests.factories import OrderFactory, SparePartOrderFactory


@pytest.mark.django_db
def test_can_update_order(client, service_register, create_user_token):
    order = OrderFactory.create(services=(service_register,))
    spare_part_order = SparePartOrderFactory.create(order=order)

    data = {
        "is_paid": True,
        "sparepartorder_set": [
            {
                "id": spare_part_order.id,
                "amount": 20
            },
        ],
        "services": [
            service_register.id,
        ]

    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.put(
        f"/orders/order/{order.id}/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["is_paid"]
    assert len(response.data["sparepartorder_set"]) == 1
    assert response.data["sparepartorder_set"][0]["amount"] == 20
    assert response.data["final_bill"] == spare_part_order.spare_part.price * 20 + service_register.price
