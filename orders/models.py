from django.db import models

from cars.models import DatesModelMixin, Car


# Create your models here.
class SparePartRegister(DatesModelMixin):
    """Модель реестра запчастей"""

    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"

    car_model = models.CharField(verbose_name="Модель авто", max_length=100)
    car_brand = models.CharField(verbose_name="Марка авто", max_length=100)
    price = models.PositiveIntegerField(verbose_name="Цена запчасти")
    name = models.CharField(verbose_name="Название запчасти", max_length=100)
    amount = models.PositiveIntegerField(verbose_name="Количество запчастей")

    def __str__(self):
        return self.name


class Purchase(DatesModelMixin):
    """Модель закупки"""

    class Meta:
        verbose_name = "Закупка"
        verbose_name_plural = "Закупки"

    delivery_date = models.DateTimeField(verbose_name="Дата поставки")
    supplier = models.CharField(verbose_name="Поставщик", max_length=100)

    def __str__(self):
        return self.id


class SparePartPurchase(DatesModelMixin):
    """Модель запчасти, включенные в закупку"""

    class Meta:
        unique_together = ("spare_part", "purchase")
        verbose_name = "Запчасть, включенная в закупку"
        verbose_name_plural = "Запчасти, включенные в закупки"

    spare_part = models.ForeignKey(
        SparePartRegister,
        verbose_name="Запчасть",
        on_delete=models.PROTECT,
    )
    purchase = models.ForeignKey(
        Purchase,
        verbose_name="Закупка",
        on_delete=models.CASCADE,
    )

    cost = models.PositiveIntegerField(verbose_name="Себестоимость запчасти")
    amount = models.PositiveIntegerField(verbose_name="Количество запчастей")


class ServiceRegister(DatesModelMixin):
    """Модель реестра услуг"""

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    price = models.PositiveIntegerField(verbose_name="Цена услуги")
    name = models.CharField(verbose_name="Название услуги", max_length=100)

    def __str__(self):
        return self.name


class Order(DatesModelMixin):
    """Модель заказа"""

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    final_bill = models.PositiveIntegerField(verbose_name="Итоговый счет", default=0)
    is_paid = models.BooleanField(verbose_name="Отметка об оплате", default=False)
    car = models.ForeignKey(Car, verbose_name="Автомобиль", on_delete=models.PROTECT)
    services = models.ManyToManyField(ServiceRegister, verbose_name="Услуги")

    def __str__(self):
        return self.id


class SparePartOrder(DatesModelMixin):
    """Модель запчасти, включенные в заказ"""

    class Meta:
        unique_together = ("spare_part", "order")
        verbose_name = "Запчасть, включенная в закупку"
        verbose_name_plural = "Запчасти, включенная в закупки"

    spare_part = models.ForeignKey(
        SparePartRegister,
        verbose_name="Запчасть",
        on_delete=models.PROTECT,
    )
    order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        on_delete=models.CASCADE,
    )

    amount = models.PositiveIntegerField(verbose_name="Количество запчастей")
