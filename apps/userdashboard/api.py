from django.db.models import Exists
from django.db.models import ExpressionWrapper
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models.fields import BooleanField
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import BooleanFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.comments.models import Comment
from adhocracy4.projects.models import Project
from apps.classifications.models import AIClassification
from apps.classifications.models import UserClassification
from apps.notifications.emails import NotifyCreatorOnModeratorBlocked
from apps.projects import helpers

from . import serializers


class PendingNotificationsFilter(FilterSet):
    has_pending_notifications = BooleanFilter(
        field_name='has_pending_notifications')

    class Meta:
        model = Comment
        fields = ['has_pending_notifications']


class ModerationCommentViewSet(mixins.ListModelMixin,
                               mixins.UpdateModelMixin,
                               viewsets.GenericViewSet):

    serializer_class = serializers.ModerationCommentSerializer
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PendingNotificationsFilter

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

    def get_queryset(self):
        all_comments_project = helpers.get_all_comments_project(self.project)
        pending_ai_classifications = AIClassification.objects.filter(
            is_pending=True,
            comment__pk=OuterRef('pk')
        )
        pending_user_classifications = UserClassification.objects.filter(
            is_pending=True,
            comment__pk=OuterRef('pk')
        )
        return all_comments_project.filter(
            Q(user_classifications__isnull=False) |
            Q(ai_classifications__isnull=False)
        ).distinct().annotate(
            has_pending_notifications=ExpressionWrapper(
                Exists(pending_user_classifications) |
                Exists(pending_ai_classifications),
                output_field=BooleanField())
        ).order_by('-created')

    def update(self, request, *args, **kwargs):
        if 'is_blocked' in self.request.data and request.data['is_blocked']:
            NotifyCreatorOnModeratorBlocked.send(self.get_object())
        return super().update(request, *args, **kwargs)

    @action(detail=True)
    def archive(self, request, **kwargs):
        comment = self.get_object()
        for classification in comment.ai_classifications.filter(
                is_pending=True):
            classification.is_pending = False
            classification.save()
        for classification in comment.user_classifications.filter(
                is_pending=True):
            classification.is_pending = False
            classification.save()

        serializer = self.get_serializer(comment)

        return Response(data=serializer.data, status=200)

    @action(detail=True)
    def unarchive(self, request, **kwargs):
        comment = self.get_object()
        for classification in comment.ai_classifications.filter(
                is_pending=False):
            classification.is_pending = True
            classification.save()
        for classification in comment.user_classifications.filter(
                is_pending=False):
            classification.is_pending = True
            classification.save()

        serializer = self.get_serializer(comment)

        return Response(data=serializer.data, status=200)
