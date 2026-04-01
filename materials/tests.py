from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from users.models import Subscription

User = get_user_model()

class CourseLessonTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@test.com', password='testpass')
        self.moderator = User.objects.create_user(email='mod@test.com', password='testpass')
        # Создаём группу модераторов
        from django.contrib.auth.models import Group
        mod_group, _ = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(mod_group)

        self.course = Course.objects.create(title='Test Course', description='desc', owner=self.user)
        self.lesson = Lesson.objects.create(
            title='Lesson 1',
            description='desc',
            video_link='https://youtube.com/watch?v=abc',
            course=self.course,
            owner=self.user
        )

    def test_course_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)  # пагинация

    def test_course_create(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'New Course', 'description': 'New desc'}
        response = self.client.post(reverse('course-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.id)

    def test_course_update_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.patch(url, {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated')

    def test_course_update_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.patch(url, {'title': 'Updated by mod'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated by mod')

    def test_course_delete_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_course_delete_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_video_link_validation(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Invalid Lesson',
            'description': 'desc',
            'video_link': 'https://example.com/video',
            'course': self.course.id
        }
        response = self.client.post(reverse('lesson-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)

    def test_lesson_video_link_valid(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Valid Lesson',
            'description': 'desc',
            'video_link': 'https://youtube.com/watch?v=valid',
            'course': self.course.id
        }
        response = self.client.post(reverse('lesson-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
