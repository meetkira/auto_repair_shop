from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers

from orders.models import SparePartRegister, Purchase, SparePartPurchase


# ---------------- SparePartRegister
class SparePartCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = SparePartRegister
        read_only_fields = ("id", "created", "updated", )
        fields = "__all__"


class SparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePartRegister
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", )


# ---------------- Purchase
class SparePartPurchaseSerializer(serializers.ModelSerializer):
    """Сериализатор для запчасти закупки"""
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(validators=[MinValueValidator(1, "Purchase must contain at least 1 spare part")])

    class Meta:
        model = SparePartPurchase
        fields = ("id", "amount", "cost")
        read_only_fields = ("cost", )


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
                raise serializers.ValidationError({"spare part error": "Spare part doesn't exist or not enough spare parts in stock"})
        return purchase

    class Meta:
        model = Purchase
        read_only_fields = ("id", "created", "updated",)
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    sparepartpurchase_set = SparePartPurchaseSerializer(many=True)

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data): # TODO: переделать!
        sparepartpurchases = validated_data.pop("sparepartpurchase_set")

        sparepartpurchases_by_id = {sparepartpurchase["id"]: sparepartpurchase for sparepartpurchase in sparepartpurchases}
        old_sparepartpurchases = instance.sparepartpurchase_set
        with transaction.atomic():
            for old_sparepartpurchase in old_sparepartpurchases:
                if old_sparepartpurchase.id not in sparepartpurchases_by_id:
                    old_sparepartpurchase.delete()
                else:
                    if (
                            old_sparepartpurchase.amount
                            != sparepartpurchases_by_id[old_sparepartpurchase.id]["amount"]
                    ):
                        old_sparepartpurchase.amount = sparepartpurchases_by_id[old_sparepartpurchase.id][
                            "amount"
                        ]
                        old_sparepartpurchase.save()
                    sparepartpurchases_by_id.pop(old_sparepartpurchase.id)
            for new_sparepartpurchase in sparepartpurchases_by_id.values():
                db_spare_part = SparePartRegister.objects.get(id=new_sparepartpurchase.get("id"))
                if db_spare_part and db_spare_part.amount >= sparepartpurchases_by_id[new_sparepartpurchase]["amount"]:
                    SparePartPurchase.objects.create(
                        purchase=instance, spare_part=db_spare_part, cost=db_spare_part.price, amount=sparepartpurchases_by_id[new_sparepartpurchase]["amount"],
                    )

            instance.title = validated_data["title"]
            instance.save()

        return instance


