from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status
from django.urls import reverse

from lms.models import Lesson, Course
from users.models import User


class LessonListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@email.ru',
            phone='77777',
            city='Solikamsk')
        self.course = Course.objects.create(
            name='Как стать драконом',
            description='После окончания курса будешь настоящим драконом')
        self.lesson = Lesson.objects.create(
            name='Очешуение',
            description='Урок покрытия чешуйками',
            course=self.course,
            owner=self.user)
        self.lesson2 = Lesson.objects.create(
            name='Охвостенение',
            description='урок по отращиванию хвоста',
            course=self.course,
            owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_get_list(self):
        url = reverse('course:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lesson(self):
        url = reverse('course:lesson-get', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Очешуение')

    def test_create_lesson(self):
        self.data = {
            'name': 'Окрыление',
            'description': 'Урок по отращиванию крыльев',
            'course': 1,
            'owner': 1}
        url = reverse('course:lesson-create')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson(self):
        url = reverse('course:lesson-update', kwargs={'pk': self.lesson.pk})
        self.data = {'name': 'Покрытие чешуей'}
        response = self.client.patch(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        url = reverse('course:lesson-delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Exception):
            Lesson.objects.get(pk=self.lesson.pk)
