from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, IndividualUser, EntityUser
from users.permissions import IsWorker, IsWorkerOrCurrent
from users.serializers import IndividualUserRegistrationSerializer, EntityUserRegistrationSerializer, \
    IndividualUserSerializer, EntityUserSerializer, ChangePasswordSerializer


# Create your views here.

class ChangePasswordView(UpdateAPIView):
    """Смена пароля пользователя"""
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


# ----------------Individual
class IndividualUserCreateView(CreateAPIView):
    """Создание пользователя физ лица"""
    serializer_class = IndividualUserRegistrationSerializer
    permission_classes = [AllowAny]


class IndividualUserListView(ListAPIView):
    """Получение списка физ лиц"""
    serializer_class = IndividualUserSerializer
    permission_classes = [IsWorker]

    def get_queryset(self):
        return User.objects.filter(type=User.Types.INDIVIDUAL)


class IndividualUserView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление физ лиц"""
    model = IndividualUser
    serializer_class = IndividualUserSerializer
    permission_classes = [IsWorkerOrCurrent]

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
    permission_classes = [IsWorker]

    def get_queryset(self):
        return User.objects.filter(type=User.Types.ENTITY)


class EntityUserView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление юр лиц"""
    model = EntityUser
    serializer_class = EntityUserSerializer
    permission_classes = [IsWorkerOrCurrent]

    def get_object(self):
        obj = self.request.user
        return obj
