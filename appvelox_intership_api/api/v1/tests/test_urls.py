from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone as tz
from rest_framework import status
import random
from rest_framework.test import APIClient, APITestCase

from tasks.models import Task
from ultis.test_data_constructor import TestDataConstructor

from ..serializers import TaskSerializers

PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')

User = get_user_model()


class TaskSerializersTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_shell = TestDataConstructor()
        test_shell.create_users(2)
        test_shell.create_tasks(10)
        cls.task = test_shell.get_tasks()
        cls.user_1, cls.user_2 = test_shell.get_users()

    def setUp(self):
        self.guest_client = APIClient()
        self.authenticated_client_1 = APIClient()
        self.authenticated_client_2 = APIClient()
        self.authenticated_client_1.force_authenticate(self.user_1)
        self.authenticated_client_2.force_authenticate(self.user_2)

    def test_signnup(self):
        """Проверка создания пользователя."""
        users_count = User.objects.count()
        url = reverse('api_v1:signup')
        data = {
            'username': 'New_user',
            'password': User.objects.make_random_password()
        }
        response = self.guest_client.post(url, data=data, format='json')
        self.assertEqual(User.objects.count(), users_count + 1)
        new_user = User.objects.last()
        self.assertEqual(new_user.username, data['username'])
        self.assertTrue(new_user.check_password(data['password']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_create(self):
        """Проверка создания задачи."""
        tasks_count = Task.objects.count()
        url = reverse('api_v1:tasks_create')
        data = {
            'deadline': tz.now(),
            'title': 'New Task',
            'description': 'Test description'
        }
        response = self.authenticated_client_1.post(
            url,
            data=data,
            format='json'
        )
        self.assertEqual(Task.objects.count(), tasks_count + 1)
        new_post = Task.objects.first()
        default_is_finished = False
        compared_names = (
            (data['title'], new_post.title),
            (data['deadline'], new_post.deadline),
            (data['description'], new_post.description),
            (default_is_finished, new_post.is_finished)
        )
        for expected_name, test_name in compared_names:
            with self.subTest(expected_name=expected_name):
                self.assertEqual(expected_name, test_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_show_tasks(self):
        """Проверка просмтотра списка задач."""
        url = reverse('api_v1:tasks_show-list')
        tasks_user = self.user_1.tasks.all()
        response = self.authenticated_client_1.get(url, format='json')
        serializer = TaskSerializers(tasks_user[:PAGE_SIZE], many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_task(self):
        """Проверка просмтотра конкретной задачи."""
        tasks_user = self.user_1.tasks.all()
        for i, task_user in enumerate(tasks_user, 1):
            with self.subTest(task_user=task_user):
                url = reverse('api_v1:tasks_show-detail', kwargs={'pk': i})
                response = self.authenticated_client_1.get(url, format='json')
                serializer = TaskSerializers(task_user)
                self.assertEqual(response.data, serializer.data)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        """Проверка удаления задачи."""
        tasks_user = self.user_1.tasks.all()
        tasks_user_count = self.user_1.tasks.all().count()
        for i, task_user in enumerate(tasks_user, 1):
            with self.subTest(task_user=task_user):
                url = reverse('api_v1:tasks_delete', kwargs={'pk': i})
                response = self.authenticated_client_1.delete(
                    url,
                    format='json'
                )
                self.assertEqual(
                    response.status_code,
                    status.HTTP_204_NO_CONTENT
                )
                tasks_user_count -= 1
                self.assertEqual(
                    self.user_1.tasks.all().count(),
                    tasks_user_count
                    )

    def test_finish_task(self):
        """Проверка отметки задачи как выполненной."""
        tasks_user = self.user_1.tasks.all()
        for i, task_user in enumerate(tasks_user, 1):
            with self.subTest(task_user=task_user):
                url = reverse('api_v1:tasks_finish', kwargs={'pk': i})
                response = self.authenticated_client_1.patch(
                    url,
                    format='json'
                )
                self.assertEqual(
                    Task.objects.get(id=i).is_finished,
                    True
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated_user_get_access(self):
        """Проверка получения доступа неаутентифицированного пользовотеля."""
        urls = (reverse('api_v1:tasks_create'),
                reverse('api_v1:tasks_show-list'),
                reverse('api_v1:tasks_show-detail', kwargs={'pk': 1}),
                reverse('api_v1:tasks_finish', kwargs={'pk': 1}),
                reverse('api_v1:tasks_delete', kwargs={'pk': 1})
                )
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED
                )

    def test_show_not_your_own_tasks(self):
        """Проверка просмотра/изменения/удаления не своих задач"""
        tasks_user_2 = self.user_2.tasks.all()
        for task_user_2 in tasks_user_2:
            responses = (
                    self.authenticated_client_1.get(
                        reverse(
                            'api_v1:tasks_show-detail',
                            kwargs={'pk': task_user_2.id}
                        )),
                    self.authenticated_client_1.patch(
                        reverse(
                            'api_v1:tasks_finish',
                            kwargs={'pk': task_user_2.id}
                        )),
                    self.authenticated_client_1.delete(
                        reverse(
                            'api_v1:tasks_delete',
                            kwargs={'pk': task_user_2.id}
                        )),
                    )
            for response in responses:
                with self.subTest(response=response):
                    self.assertEqual(
                        response.status_code,
                        status.HTTP_404_NOT_FOUND
                    )
