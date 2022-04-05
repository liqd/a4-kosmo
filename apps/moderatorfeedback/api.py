from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.comments.models import Comment
from apps.moderatorfeedback.models import ModeratorCommentStatement
from apps.moderatorfeedback.serializers import \
    ModeratorCommentStatementSerializer


class ModeratorCommentStatementViewSet(mixins.CreateModelMixin,
                                       mixins.UpdateModelMixin,
                                       viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = ModeratorCommentStatementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        self.comment_pk = kwargs.get('comment_pk', '')
        return super().dispatch(request, *args, **kwargs)

    @property
    def comment(self):
        return get_object_or_404(
            Comment,
            pk=self.comment_pk
        )

    def get_permission_object(self):
        return self.comment.module

    def perform_create(self, serializer):
        serializer.save(
            comment=self.comment,
            creator=self.request.user
        )
