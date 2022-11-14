from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CreateTaskView, DeleteTaskView, FinishTaskVIew,
                    ShowTaskViewSet, SignUpView)

router = DefaultRouter()

router.register(
    'tasks/show',
    ShowTaskViewSet,
    basename='tasks_show'
)

auth_urlpatterns = [
    path(
        'auth/signup/',
        SignUpView.as_view(),
        name='signup'
        ),
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
        ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
        )
]

tasks_urlpatterns = [
    path('', include(router.urls)),
    path(
        'tasks/create/',
        CreateTaskView.as_view(),
        name='tasks_create'
        ),
    path(
        'tasks/delete/<int:pk>/',
        DeleteTaskView.as_view(),
        name='tasks_delete'
        ),
    path(
        'tasks/finish/<int:pk>/',
        FinishTaskVIew.as_view(),
        name='tasks_finish'
        )
]

urlpatterns = [
    path('', include(auth_urlpatterns)),
    path('', include(tasks_urlpatterns))
]
