from pytest_factoryboy import register

from tests.factories import IndividualUserFactory, EntityUserFactory, CarFactory, SparePartRegisterFactory, \
    PurchaseFactory, SparePartPurchaseFactory, ServiceRegisterFactory

pytest_plugins = "tests.fixtures"

register(IndividualUserFactory)
register(EntityUserFactory)
register(CarFactory)
register(SparePartRegisterFactory)
register(PurchaseFactory)
register(SparePartPurchaseFactory)
register(ServiceRegisterFactory)
