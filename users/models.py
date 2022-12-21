from typing import Optional

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required!")
        if not password:
            raise ValueError("Password field is required!")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Types(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "individual"
        ENTITY = "ENTITY", "entity"

    type = models.CharField(max_length=10, choices=Types.choices, default=Types.INDIVIDUAL)
    email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    first_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_worker = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    passport = models.CharField(max_length=11, unique=True, null=True, blank=True, validators=[
        RegexValidator(
            regex='\d{4}\s\d{6}',
            message='Invalid passport data',
            code='invalid_passport'
        ),
    ])

    title = models.CharField(verbose_name="Название компании", max_length=100)
    requisites = models.CharField(verbose_name="Реквизиты", max_length=100, unique=True, null=True, blank=True,)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.type or self.type == None:
            self.type = User.Types.INDIVIDUAL
        return super().save(*args, **kwargs)


class IndividualManager(models.Manager):
    def create_user(self, email: str, password: str, first_name: str, last_name: str, passport: str, is_worker: bool,
                    middle_name: Optional[str] = None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required!")
        if not password:
            raise ValueError("Password field is required!")
        if not passport:
            raise ValueError("Passport field is required!")
        if not first_name or not last_name:
            raise ValueError("First name and last name fields are required!")

        email = email.lower()
        user = self.model(
            email=email,
            passport=passport,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            is_worker=is_worker,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, first_name: str, last_name: str, passport: str,
                         middle_name: Optional[str] = None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            passport=passport,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            is_worker=True,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=User.Types.ENTITY)
        return queryset


class IndividualUser(User):
    class Meta:
        proxy = True

    objects = IndividualManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.INDIVIDUAL
        return super().save(*args, **kwargs)


class EntityManager(models.Manager):
    def create_user(self, email: str, password: str, title: str, requisites: str):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required!")
        if not password:
            raise ValueError("Password field is required!")
        if not title:
            raise ValueError("Title field is required!")
        if not requisites:
            raise ValueError("Requisites field is required!")
        email = email.lower()
        user = self.model(
            email=email,
            title=title,
            requisites=requisites
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=User.Types.ENTITY)
        return queryset


class EntityUser(User):
    class Meta:
        proxy = True

    objects = EntityManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.ENTITY
        return super().save(*args, **kwargs)
