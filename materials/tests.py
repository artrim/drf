from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@test.com')
        self.course = Course.objects.create(name='test_course',
                                            description='test_course_description',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name='test_lesson',
                                            description='test_lesson_description',
                                            course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson_detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.lesson.name  # 'test_lesson'
        )

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        data = {
            'name': 'new_test_lesson',
            'description': 'new_test_lesson_description',
            'course': self.course.pk,
            'url': 'youtube.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lesson_update', args=(self.lesson.pk,))
        data = {
            'name': 'new_test_lesson_2',
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'new_test_lesson_2'  # 'test_lesson'
        )

    def test_lesson_list(self):
        url = reverse('materials:lesson_list')
        response = self.client.get(url)
        # print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': 4, 'url': None, 'name': 'test_lesson', 'description': 'test_lesson_description', 'image': None,
                 'course': 3, 'owner': 3}]}
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@test.com')
        self.course = Course.objects.create(name='test_course',
                                            description='test_course_description',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse('materials:subscription')
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),  {'message': 'Подписка добавлена'})

    def test_unsubscribe(self):
        url = reverse('materials:subscription')
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),  {'message': 'Подписка удалена'})
