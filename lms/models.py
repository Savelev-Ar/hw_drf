from django.db import models


class Course(models.Model):

    name = models.CharField(
        max_length=150,
        verbose_name='Название'
    )
    preview = models.ImageField(
        upload_to='media/lms',
        blank=True,
        null=True,
        verbose_name='Изображение')
    description = models.TextField(
        verbose_name='Описание'
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='user_courses',
        verbose_name='пользователь',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']


class Lesson(models.Model):

    name = models.CharField(
        max_length=150,
        verbose_name='Название'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    preview = models.ImageField(
        upload_to='media/learning',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )

    videolink = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name='Ссылка на видео'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='user_lessons',
        verbose_name='пользователь',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name']
