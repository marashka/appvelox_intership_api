from django.contrib.auth import get_user_model
from django.utils import timezone as tz

from tasks.models import Task

User = get_user_model()


class TestDataConstructor:
    """Формирует тестовые данные данные."""

    def _init_(self):
        self._users = None
        self._tasks = None

    def create_users(self, users=1):
        """Создает список тестовых пользователей.

        Количество пользователей задается аргументом "users".
        В качестве "username" используется 'HasNoName_<номер пользователя>'.
        Пароль("password") генерируется случайным образом.
        """

        self._users = [
            User.objects.create_user(
                username='HasNoName_' + str(user + 1),
                password=User.objects.make_random_password()
            )
            for user in range(users)]

    def create_tasks(self, tasks_each_user=1):
        """Создает список тестовых задач.

        Количество задач для каждого пользователя
        задается аргументом "tasks_each_user".
        В качестве "title" используется 'Test task_<номер задачи>'.
        В качестве "description" используется 'Test description'.
        Авторы("author") берутся из списка "self._users".
        Срок выполнения задачи устанавливается в "tz.now()" с последующим
        увеличением на 1 час для каждой новой созданной задачи автора.
        """

        tasks = [
            Task(
                title=f'Test task_{str(task + 1)} {str(user.username)}',
                description='Test description',
                deadline=tz.now() + tz.timedelta(hours=delay_creat_tasks),
                author=user
            )
            for user in self._users
            for delay_creat_tasks, task in enumerate(range(tasks_each_user), 1)
        ]
        self._tasks = Task.objects.bulk_create(tasks)

    def get_users(self):
        """Выдает список тестовых пользователей."""
        return self._users

    def get_tasks(self):
        """Выдает список тестовых задач."""
        return self._tasks
