from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from ultis.exceptions import TaskAlreadyFinishedError, WrongPkTaskError

from .mixins import GetTaskMixin
from .serializers import SignupSerializer, TaskSerializers

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    """Регистрирует пользователя"""

    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return User.objects.create_user(**serializer.validated_data)


class CreateTaskView(generics.CreateAPIView):
    """Создает задачу"""

    serializer_class = TaskSerializers

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class ShowTaskViewSet(GetTaskMixin, viewsets.ReadOnlyModelViewSet):
    """Выводит список задач/задачу"""

    serializer_class = TaskSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_finished',)


class DeleteTaskView(GetTaskMixin, generics.DestroyAPIView):
    """Удаляет задачу"""

    serializer_class = TaskSerializers


class FinishTaskVIew(APIView):
    """Отмечает задачу как выполненную"""

    def patch(self, request, pk):
        try:
            task = Task.objects.get(author=request.user, id=pk)
        except ObjectDoesNotExist as error:
            raise WrongPkTaskError from error
        if task.is_finished is True:
            raise TaskAlreadyFinishedError
        task.is_finished = True
        task.save()
        serializer = TaskSerializers(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
