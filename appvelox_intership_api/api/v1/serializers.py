from django.contrib.auth import get_user_model
from rest_framework import serializers

from tasks.models import Task

User = get_user_model()


class TaskSerializers(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M',
        error_messages={
            'invalid': 'Установленная дата-время имеет неправильный формат. '
            'Пример: 2022-12-31T24:00'
            })

    class Meta:
        model = Task
        fields = ('id', 'deadline', 'title', 'description', 'is_finished')
        read_only_fields = ('is_finished',)


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
