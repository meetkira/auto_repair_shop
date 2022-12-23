from pytest_factoryboy import register

from tests.factories import IndividualUserFactory, EntityUserFactory, CarFactory, SparePartRegisterFactory, \
    PurchaseFactory, SparePartPurchaseFactory, ServiceRegisterFactory, OrderFactory, SparePartOrderFactory

pytest_plugins = "tests.fixtures"

register(IndividualUserFactory)
register(EntityUserFactory)
register(CarFactory)
register(SparePartRegisterFactory)
register(PurchaseFactory)
register(SparePartPurchaseFactory)
register(ServiceRegisterFactory)
register(OrderFactory)
register(SparePartOrderFactory)
