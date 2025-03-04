from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from lms.models import Course, Lesson


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


class Payment(models.Model):
    METHODS = (('cash', 'наличные'), ('transfer to account', 'перевод на счет'),)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь',
        blank=True,
        null=True)

    payment_date = models.DateField(
        default=timezone.now,
        verbose_name='Дата оплаты')

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Курс',
        blank=True,
        null=True)

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Урок',
        blank=True,
        null=True)

    payment_amount = models.PositiveIntegerField(
        verbose_name='Сумма платежа')

    payment_method = models.CharField(
        max_length=20,
        choices=METHODS,
        verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.paid_course if self.paid_course else self.paid_lesson} - {self.payment_amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежы'
        ordering = ['payment_date']
