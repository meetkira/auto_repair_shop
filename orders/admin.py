from django.contrib import admin

# Register your models here.
from orders.models import SparePartRegister, Purchase, SparePartPurchase, ServiceRegister, Order, SparePartOrder

admin.site.register(SparePartRegister)
admin.site.register(Purchase)
admin.site.register(SparePartPurchase)
admin.site.register(ServiceRegister)
admin.site.register(Order)
admin.site.register(SparePartOrder)
