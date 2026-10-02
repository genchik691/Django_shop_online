# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Аутентификация по email вместо username.
    """
    # ✅ Убираем поле username
    username = None

    # ✅ Email как поле для авторизации
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )

    # ✅ Дополнительные поля
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='Аватар',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        blank=True,
        null=True
    )

    # ✅ Email — поле для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


from django.db import models

# Create your models here.
