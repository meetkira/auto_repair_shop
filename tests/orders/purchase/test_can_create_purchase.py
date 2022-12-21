from datetime import datetime

import pytest


@pytest.mark.django_db
def test_can_create_purchase(client, spare_part_register, create_user_token):
    data = {
        "delivery_date": datetime.now(),
        "supplier": "test_supplier",
        "sparepartpurchase_set": [
            {
                "id": spare_part_register.id,
                "amount": 10
            },
        ],

    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.post(
        "/orders/purchases/create/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data["supplier"] == data["supplier"]
    assert len(response.data["sparepartpurchase_set"]) == 1
