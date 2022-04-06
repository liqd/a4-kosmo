from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.projects.models import Project
from apps.classifications.models import AIClassification
from apps.classifications.models import UserClassification
from apps.notifications.emails import NotifyCreatorOnModeratorBlocked
from apps.projects import helpers

from . import serializers


class ClassificationViewSet(mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['is_pending']
    lookup_field = 'pk'

    def dispatch(self, request, *args, **kwargs):
        self.project_pk = kwargs.get('project_pk', '')
        return super().dispatch(request, *args, **kwargs)

    @property
    def project(self):
        return get_object_or_404(
            Project,
            pk=self.project_pk
        )

    def get_permission_object(self):
        return self.project

    def update(self, request, *args, **kwargs):
        if 'is_blocked' in self.request.data:
            comment = self.get_object().comment
            comment.is_blocked = request.data['is_blocked']
            comment.save()
            if comment.is_blocked:
                NotifyCreatorOnModeratorBlocked.send(comment)
        return super().update(request, *args, **kwargs)


class UserClassificationViewSet(ClassificationViewSet):

    serializer_class = serializers.UserClassificationSerializer

    def get_queryset(self):
        all_comments_project = helpers.get_all_comments_project(self.project)
        return UserClassification.objects.\
            filter(comment__in=all_comments_project)\
            .order_by('created')


class AIClassificationViewSet(ClassificationViewSet):

    serializer_class = serializers.AIClassificationSerializer

    def get_queryset(self):
        all_comments_project = helpers.get_all_comments_project(self.project)
        return AIClassification.objects.\
            filter(comment__in=all_comments_project)\
            .order_by('created')
