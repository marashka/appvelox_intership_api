from django.contrib.auth import get_user_model
from django.test import TestCase

from ultis.test_data_constructor import TestDataConstructor


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_shell = TestDataConstructor()
        test_shell.create_users()
        test_shell.create_tasks()
        cls.task, = test_shell.get_tasks()
        cls.user, = test_shell.get_users()

    def test_models_have_correct_object_names(self):
        """Правильно ли отображается __str__ в объектах моделей."""
        task = TaskModelTest.task
        expected_name_task = task.title[:15]
        self.assertEqual(expected_name_task, str(task))

    def test_models_fields_have_correct_verbos_names(self):
        """Правильно ли отображаются verbose_names в объектах моделей."""
        task = TaskModelTest.task
        field_verbose_name = (
            ('title', 'Название задачи'),
            ('description', 'Описание'),
            ('deadline', 'Cрок выполненения'),
            ('is_finished', 'Задача выполнена')
        )
        for field_name, verbose_name in field_verbose_name:
            with self.subTest(field_name=field_name):
                expected_verbose_name_task = task._meta.get_field(
                    field_name
                    ).verbose_name
                self.assertEqual(expected_verbose_name_task, verbose_name)
