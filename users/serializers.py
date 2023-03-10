from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User, EntityUser, IndividualUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('id', 'email', )


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля пользователя"""
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'new_password', 'old_password',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        user = self.instance
        if not user.check_password(old_password):
            raise serializers.ValidationError({"password error": "Incorrect old password"})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance


class IndividualUserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя физ лица"""

    password = serializers.CharField(max_length=128, write_only=True, validators=[validate_password])

    class Meta:
        model = IndividualUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'passport', 'is_worker', 'middle_name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = IndividualUser.objects.create(
            passport=validated_data['passport'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data.get('middle_name'),
            is_worker=validated_data['is_worker'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class IndividualUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualUser
        fields = ['id', "email", "passport", "first_name", "middle_name", "last_name", "is_worker", "is_active"]
        read_only_fields = ('id',)


class EntityUserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя юр лица"""

    password = serializers.CharField(max_length=128, write_only=True, validators=[validate_password])

    class Meta:
        model = EntityUser
        fields = ('id', 'title', 'requisites', 'email', 'password', )
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = EntityUser.objects.create(
            title=validated_data['title'],
            email=validated_data['email'],
            requisites=validated_data['requisites'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class EntityUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityUser
        fields = ['id', "email", "title", "requisites"]
        read_only_fields = ('id',)
