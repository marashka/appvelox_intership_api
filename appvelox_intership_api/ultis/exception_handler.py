from rest_framework.views import exception_handler


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)
    handlers = {
        'AuthenticationFailed': _handle_authentication_failed_error,
        'NotAuthenticated': _handle_no_authentication_failed_error,
        'InvalidToken': _handle_invalid_token_error,
    }
    response = exception_handler(exception, context)
    exception_class = exception.__class__.__name__

    if response is not None:
        response.data['status_code'] = response.status_code
    if exception_class in handlers:
        return handlers[exception_class](exception, context, response)
    return response


def _handle_authentication_failed_error(exception, context, response):
    response.data = {
        'error': (
            'Не найдена активная учетная запись с '
            'указанными учетными данными'
            ),
        'status': response.status_code
    }
    return response


def _handle_no_authentication_failed_error(exception, context, response):
    response.data = {
        'error': (
            'JWT токен не был предоставлен для аутентификации'
            ),
        'status': response.status_code
    }
    return response


def _handle_invalid_token_error(exception, context, response):
    response.data = {
        'error': (
            'Предоставленный токен невалиден'
            ),
        'status': response.status_code
    }
    return response
