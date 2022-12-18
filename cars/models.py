from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from users.models import User


# Create your models here.
class DatesModelMixin(models.Model):
    """Базовая модель"""
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Car(DatesModelMixin):
    """Модель автомобиля"""
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    model = models.CharField(verbose_name="Модель авто", max_length=100)
    brand = models.CharField(verbose_name="Марка авто", max_length=100)
    number = models.CharField(verbose_name="Номер авто", max_length=9, validators=[
        RegexValidator(
            regex='/^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}$/ui',
            message='Invalid car number',
            code='invalid_car_number'
        ),
    ])
    color = models.CharField(verbose_name="Цвет авто", max_length=100)
    user = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.PROTECT)

    def __str__(self):
        return self.number
