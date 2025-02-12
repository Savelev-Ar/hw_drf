from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электрической почты',
        help_text='Укажите адрес электрической почты')

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name='Телефон',
        help_text='Укажите номер телефона')

    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Город',
        help_text='Укажите название города')

    avatar = models.ImageField(
        upload_to='users/avatars',
        blank=True,
        null=True,
        verbose_name='Аватар',
        help_text='Загрузите аватара')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'
