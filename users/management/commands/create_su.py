from django.core.management import BaseCommand

from users.models import User, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_active=True,
            is_superuser=True
        )

        user.set_password('admin')
        user.save()
