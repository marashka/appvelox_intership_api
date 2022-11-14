from rest_framework import status
from rest_framework.exceptions import APIException


class SecretKeyError(Exception):
    """Вызывается, когда отсутствует SECRET_KEY."""

    def __init__(self):
        super().__init__('В переменных окружения отсутствует SECRET_KEY.')


class TaskAlreadyFinishedError(APIException):
    """Вызывается, когда confirmation code невалидный."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Задача уже отмечена как выполненная'
    default_code = 'invalid_confirmation_code'


class WrongPkTaskError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = (
        'Проверьте pk в url адрессе, '
        'в Вашем списке задач нет задачи с таким pk'
        )
    default_code = 'invalid_pk'
