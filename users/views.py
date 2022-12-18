from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, IndividualUser, EntityUser
from users.serializers import IndividualUserRegistrationSerializer, EntityUserRegistrationSerializer, \
    IndividualUserSerializer, EntityUserSerializer


# Create your views here.

# ----------------Individual
class IndividualUserCreateView(CreateAPIView):
    """Создание пользователя физ лица"""
    serializer_class = IndividualUserRegistrationSerializer
    permission_classes = [AllowAny]


class IndividualUserListView(ListAPIView):
    """Получение списка физ лиц"""
    serializer_class = IndividualUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(type=User.Types.INDIVIDUAL)


class IndividualUserView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление физ лиц"""
    model = IndividualUser
    serializer_class = IndividualUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.request.user
        return obj


# ----------------Entity
class EntityUserCreateView(CreateAPIView):
    """Создание пользователя юр лица"""
    serializer_class = EntityUserRegistrationSerializer
    permission_classes = [AllowAny]


class EntityUserListView(ListAPIView):
    """Получение списка юр лиц"""
    serializer_class = EntityUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(type=User.Types.ENTITY)


class EntityUserView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление юр лиц"""
    model = EntityUser
    serializer_class = EntityUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.request.user
        return obj
