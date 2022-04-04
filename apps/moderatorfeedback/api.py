from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.permissions import ViewSetRulesPermission
from apps.contrib.api import CommentMixin
from apps.moderatorfeedback.models import ModeratorCommentStatement
from apps.moderatorfeedback.serializers import \
    ModeratorCommentStatementSerializer


class ModeratorCommentStatementViewSet(CommentMixin,
                                       mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.UpdateModelMixin,
                                       viewsets.GenericViewSet):
    serializer_class = ModeratorCommentStatementSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        return self.comment

    def get_queryset(self):
        return ModeratorCommentStatement.objects.filter(
            comment=self.comment)
