from rest_framework import serializers

from apps.moderatorfeedback.models import ModeratorCommentStatement


class ModeratorCommentStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorCommentStatement
        fields = ['statement', 'comment']
