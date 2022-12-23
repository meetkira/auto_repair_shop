from datetime import datetime

import pytest


@pytest.mark.django_db
def test_can_update_purchase(client, spare_part_purchase, create_user_token):
    data = {
        "delivery_date": datetime.now(),
        "supplier": "update_supplier",
        "sparepartpurchase_set": [
            {
                "id": spare_part_purchase.spare_part.id,
                "amount": 20
            },
        ],

    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.put(
        f"/orders/purchases/purchase/{spare_part_purchase.purchase.id}/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["supplier"] == data["supplier"]
    assert len(response.data["sparepartpurchase_set"]) == 1
    assert response.data["sparepartpurchase_set"][0]["amount"] == 20
