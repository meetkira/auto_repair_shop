from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from cars.models import Car
from cars.permissions import IsWorkerOrOwner
from cars.serializers import CarCreateSerializer, CarSerializer
from users.permissions import IsWorker


class CarCreateView(CreateAPIView):
    """Создание автомобиля"""
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer
    permission_classes = [IsWorkerOrOwner]


class CarListView(ListAPIView):
    """Получение списка автомобилей"""
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsWorker]


class UsersCarListView(ListAPIView):
    """Получение списка автомобилей пользователя"""
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsWorkerOrOwner]

    def get_queryset(self):
        return Car.objects.filter(user_id=self.request.user.id)


class CarView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление автомобиля"""
    model = Car
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsWorkerOrOwner]
