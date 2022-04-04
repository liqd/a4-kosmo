from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

# from adhocracy4.api.permissions import ViewSetRulesPermission
from apps.moderatorfeedback.models import ModeratorCommentStatement
from apps.moderatorfeedback.serializers import \
    ModeratorCommentStatementSerializer


class ModeratorCommentStatementViewSet(mixins.CreateModelMixin,
                                       viewsets.GenericViewSet):
    serializer_class = ModeratorCommentStatementSerializer
    # permission_classes = (ViewSetRulesPermission,)
    queryset = ModeratorCommentStatement.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    # def get_permission_object(self):
    #     return self.comment

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )
