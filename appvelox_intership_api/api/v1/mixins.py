from django.http import Http404

from ultis.exceptions import WrongPkTaskError


class GetTaskMixin:
    def get_object(self):
        try:
            return super().get_object()
        except Http404 as error:
            raise WrongPkTaskError from error

    def get_queryset(self):
        author = self.request.user
        return author.tasks.all()
