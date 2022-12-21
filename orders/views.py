from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView

from orders.models import SparePartRegister, Purchase
from orders.serializers import SparePartCreateSerializer, SparePartSerializer, PurchaseCreateSerializer, \
    PurchaseSerializer
from users.permissions import IsWorker


# Create your views here.
# ---------------- SparePartRegister
class SparePartCreateView(CreateAPIView):
    """Создание запчасти в реестре запчастей"""
    queryset = SparePartRegister.objects.all()
    serializer_class = SparePartCreateSerializer
    permission_classes = [IsWorker]


class SparePartListView(ListAPIView):
    """Получение реестра запчастей"""
    queryset = SparePartRegister.objects.all()
    serializer_class = SparePartSerializer
    permission_classes = [IsWorker]


class SparePartView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление запчасти из реестра"""
    model = SparePartRegister
    queryset = SparePartRegister.objects.all()
    serializer_class = SparePartSerializer
    permission_classes = [IsWorker]


# ---------------- Purchase
class PurchaseCreateView(CreateAPIView):
    """Создание закупки"""
    queryset = Purchase.objects.all()
    serializer_class = PurchaseCreateSerializer
    permission_classes = [IsWorker]


class PurchaseListView(ListAPIView):
    """Получение списка закупок"""
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsWorker]


class PurchaseView(RetrieveUpdateDestroyAPIView):
    """Получение/удаление закупки"""
    model = Purchase
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsWorker]

'''class PurchaseView(RetrieveDestroyAPIView):
    """Получение/удаление закупки"""
    model = Purchase
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsWorker]'''
