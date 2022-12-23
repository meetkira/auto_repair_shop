import pytest


@pytest.mark.django_db
def test_can_create_order(client, spare_part_register, service_register, car, create_user_token):
    data = {
        "is_paid": False,
        "car": car.id,
        "sparepartorder_set": [
            {
                "id": spare_part_register.id,
                "amount": 10
            },
        ],
        "services": [
            service_register.id,
        ]

    }
    bearer = {'HTTP_AUTHORIZATION': f'Bearer {create_user_token}'}

    response = client.post(
        "/orders/create/",
        data=data,
        **bearer,
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data["final_bill"] == spare_part_register.price * 10 + service_register.price
    assert len(response.data["sparepartorder_set"]) == 1
    assert len(response.data["services"]) == 1
