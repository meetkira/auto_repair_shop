from datetime import datetime

import factory.django

from cars.models import Car
from orders.models import SparePartRegister, Purchase, SparePartPurchase, ServiceRegister, Order, SparePartOrder
from users.models import IndividualUser, EntityUser


class IndividualUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IndividualUser

    email = "testindividualuser@ya.ru"
    first_name = "first_name"
    middle_name = "middle_name"
    last_name = "last_name"
    passport = "1234 567890"
    is_worker = True
    password = factory.PostGenerationMethodCall('set_password', 'testuserpassword')


class EntityUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EntityUser

    email = "testentityuser@ya.ru"
    title = "title"
    requisites = "1234567890"
    password = factory.PostGenerationMethodCall('set_password', 'testuserpassword')


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car

    model = "test_model"
    brand = "test_brand"
    number = "А123КМ45"
    color = "test_color"
    user = factory.SubFactory(IndividualUserFactory)


class SparePartRegisterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SparePartRegister

    car_model = "test_model"
    car_brand = "test_brand"
    price = 1000
    name = "test_name"
    amount = 100


class PurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Purchase

    delivery_date = datetime.now()
    supplier = "test_supplier"


class SparePartPurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SparePartPurchase

    cost = 1000
    amount = 10
    spare_part = factory.SubFactory(SparePartRegisterFactory)
    purchase = factory.SubFactory(PurchaseFactory)


class ServiceRegisterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServiceRegister

    price = 1000
    name = "test_name"


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    final_bill = 10000
    is_paid = False
    car = factory.SubFactory(CarFactory)

    @factory.post_generation
    def services(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for service in extracted:
                self.services.add(service)


class SparePartOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SparePartOrder

    amount = 5
    spare_part = factory.SubFactory(SparePartRegisterFactory)
    order = factory.SubFactory(OrderFactory)
