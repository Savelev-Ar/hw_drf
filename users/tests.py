from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status
from django.urls import reverse

from lms.models import Course
from users.models import User, Subscribe


class SubscribeDeleteTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@email.ru',
            phone='77777',
            city='Solikamsk')
        self.course = Course.objects.create(
            name='Как стать драконом',
            description='После окончания курса будешь настоящим драконом')
        self.subscribe = Subscribe.objects.create(
            user=self.user,
            course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_create_subscribe(self):
        existed_sub = Subscribe.objects.get(user_id=self.user.pk, course_id=self.course.pk)
        existed_sub.delete()
        self.data = {'user': self.user.pk, 'course': self.course.pk}
        url = reverse('users:subscribes', kwargs={'user_id': self.user.pk})
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscribe.objects.get(user=self.user, course=self.course))

    def test_delete_subscribe(self):
        url = reverse('users:subscribes', kwargs={'user_id': self.user.pk})
        self.data = {'user': self.user.pk, 'course': self.course.pk}
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(Exception):
            Subscribe.objects.get(pk=self.subscribe.pk)
