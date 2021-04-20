from rest_framework import permissions
from rest_framework import viewsets

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project
from apps.projects.serializers import ProjectSerializer

from .serializers import AppModuleSerializer
from .serializers import AppProjectSerializer
from . import helpers


class AppProjectsViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AppProjectSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Project.objects.filter(
            is_draft=False,
            is_archived=False,
            is_app_accessible=True)


class AppModuleViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AppModuleSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Module.objects.filter(
            is_draft=False,
            project__is_app_accessible=True
        )


class ModerationProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        project_offensive_count = \
            {project: helpers.get_num_classifications(project)
             for project in list(self.request.user.project_moderator.all())}
        return sorted(project_offensive_count,
                      key=project_offensive_count.get,
                      reverse=True)
