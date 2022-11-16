from django.contrib.auth import get_user_model
from django.utils import timezone as tz
from tasks.models import Task

User = get_user_model()

TEST_USER_PASSWORD = User.objects.make_random_password()


class TestDataConstructor:
    def _init_(self):
        self._users = None
        self._tasks = None

    def create_users(self, users=1):
        self._users = [
            User.objects.create_user(
                username='HasNoName_' + str(user + 1),
                password=TEST_USER_PASSWORD
            )
            for user in range(users)]

    def create_tasks(self, tasks_each_user=1):
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
        return self._users

    def get_tasks(self):
        return self._tasks
