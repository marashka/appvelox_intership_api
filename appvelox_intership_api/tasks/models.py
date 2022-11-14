from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DateTimeField

from django.conf import settings

User = get_user_model()


class Task(models.Model):
    """Список задач"""

    title = models.CharField(
        max_length=256,
        verbose_name='Название задачи'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Автор'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    deadline = DateTimeField(verbose_name='Cрок выполненения')
    is_finished = models.BooleanField(
        default=False,
        verbose_name='Задача выполнена'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('deadline', )

    def __str__(self):
        return self.title[:settings.TEXT_TITLE_LENGTH]
