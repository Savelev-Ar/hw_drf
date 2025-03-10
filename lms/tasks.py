from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lms.models import Course
from users.models import User


@shared_task
def send_email(course_id):
    course = Course.objects.get(pk=course_id)
    subscribes = course.subscribes.all()
    recipient_list = [subscribe.user.email for subscribe in subscribes]
    send_mail('Обновление курса',
              f'Курс "{course.name}" обновлен. Посетите наш сайт для более подробной информации',
              EMAIL_HOST_USER,
              recipient_list,
              fail_silently=False)


@shared_task
def check_active_user():
    user_set = User.objects.all()
    for user in user_set:
        if user.last_login:
            if (timezone.now() - user.last_login) >= timedelta(days=30):
                user.is_active = False
                user.save()
