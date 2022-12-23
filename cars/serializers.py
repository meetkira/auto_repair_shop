from rest_framework import serializers

from cars.models import Car
from users.models import User
from users.serializers import UserSerializer


class CarCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    number = serializers.RegexField(regex=r'^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}', required=True)
    user = serializers.SlugRelatedField(
        required=True,
        queryset=User.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Car
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
