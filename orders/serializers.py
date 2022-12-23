from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers

from cars.models import Car
from cars.serializers import CarSerializer
from orders.models import SparePartRegister, Purchase, SparePartPurchase, ServiceRegister, SparePartOrder, Order


# ---------------- SparePartRegister
class SparePartCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = SparePartRegister
        read_only_fields = ("id", "created", "updated",)
        fields = "__all__"


class SparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePartRegister
        fields = "__all__"
        read_only_fields = ("id", "created", "updated",)


# ---------------- Purchase
class SparePartPurchaseSerializer(serializers.ModelSerializer):
    """Сериализатор для запчасти закупки"""
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(validators=[MinValueValidator(1, "Purchase must contain at least 1 spare part")])

    class Meta:
        model = SparePartPurchase
        fields = ("id", "amount", "cost")
        read_only_fields = ("cost",)


class PurchaseCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    sparepartpurchase_set = SparePartPurchaseSerializer(many=True)

    def create(self, validated_data):
        spare_parts = validated_data.pop("sparepartpurchase_set")
        purchase = Purchase.objects.create(**validated_data)
        for spare_part in spare_parts:
            db_spare_part = SparePartRegister.objects.get(id=spare_part.get("id"))
            if db_spare_part and db_spare_part.amount >= spare_part["amount"]:
                SparePartPurchase.objects.create(
                    purchase=purchase, spare_part=db_spare_part, cost=db_spare_part.price, amount=spare_part["amount"],
                )
            else:
                raise serializers.ValidationError(
                    {"spare part error": "Spare part doesn't exist or not enough spare parts in stock"})
        return purchase

    class Meta:
        model = Purchase
        read_only_fields = ("id", "created", "updated",)
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    sparepartpurchase_set = SparePartPurchaseSerializer(many=True, required=False)

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def is_valid(self, raise_exception=False):
        self._spare_parts = self.initial_data.pop('sparepartpurchase_set')
        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        for spare_part in self._spare_parts:
            db_spare_part = SparePartRegister.objects.get(id=spare_part.get("id"))
            if db_spare_part and db_spare_part.amount >= spare_part["amount"]:
                SparePartPurchase.objects.update_or_create(
                    purchase=instance, spare_part=db_spare_part, cost=db_spare_part.price,
                    defaults={"amount": spare_part["amount"]},
                )
            else:
                raise serializers.ValidationError(
                    {"spare part error": "Spare part doesn't exist or not enough spare parts in stock"})
        instance.delivery_date = validated_data["delivery_date"]
        instance.supplier = validated_data["supplier"]
        instance.save()
        return instance


# ---------------- ServiceRegister
class ServiceCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ServiceRegister
        read_only_fields = ("id", "created", "updated",)
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRegister
        fields = "__all__"
        read_only_fields = ("id", "created", "updated",)


# ---------------- Order
class SparePartOrderSerializer(serializers.ModelSerializer):
    """Сериализатор для запчасти заказа"""
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(validators=[MinValueValidator(1, "Purchase must contain at least 1 spare part")])

    class Meta:
        model = SparePartOrder
        fields = ("id", "amount")


class OrderCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    sparepartorder_set = SparePartOrderSerializer(many=True, required=False)
    services = serializers.PrimaryKeyRelatedField(queryset=ServiceRegister.objects.all(), many=True, required=False)
    car = serializers.SlugRelatedField(
        required=True,
        queryset=Car.objects.all(),
        slug_field='id'
    )

    def is_valid(self, raise_exception=False):
        self._services = self.initial_data.pop('services')
        self._spare_parts = self.initial_data.pop('sparepartorder_set')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        for spare_part in self._spare_parts:
            db_spare_part = SparePartRegister.objects.get(id=spare_part.get("id"))
            if db_spare_part and db_spare_part.amount >= spare_part["amount"]:
                SparePartOrder.objects.create(
                    order=order, spare_part=db_spare_part, amount=spare_part["amount"],
                )
                order.final_bill += db_spare_part.price * spare_part["amount"]
            else:
                raise serializers.ValidationError(
                    {"spare part error": "Spare part doesn't exist or not enough spare parts in stock"}
                )
        for service_id in self._services:
            service = ServiceRegister.objects.get(id=service_id)
            order.services.add(service)
            order.final_bill += service.price
        return order

    class Meta:
        model = Order
        read_only_fields = ("id", "created", "updated", "final_bill")
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    sparepartorder_set = SparePartOrderSerializer(many=True, required=False)
    services = ServiceSerializer(many=True, required=False)
    car = CarSerializer(read_only=True)

    def is_valid(self, raise_exception=False):
        self._services = self.initial_data.pop('services')
        self._spare_parts = self.initial_data.pop('sparepartorder_set')
        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        instance.final_bill = 0
        for spare_part in self._spare_parts:
            db_spare_part = SparePartRegister.objects.get(id=spare_part.get("id"))
            if db_spare_part and db_spare_part.amount >= spare_part["amount"]:
                SparePartOrder.objects.update_or_create(
                    order=instance, spare_part=db_spare_part, defaults={"amount": spare_part["amount"]},
                )
                instance.final_bill += db_spare_part.price * spare_part["amount"]
            else:
                raise serializers.ValidationError(
                    {"spare part error": "Spare part doesn't exist or not enough spare parts in stock"})
        for service_id in self._services:
            service = ServiceRegister.objects.get(id=service_id)
            instance.final_bill += service.price
            if service not in instance.services.all():
                instance.services.add(service)

        instance.is_paid = validated_data["is_paid"]
        instance.save()
        return instance

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("id", "created", "updated",)
