from rest_framework import serializers

from adhocracy4.comments.models import Comment
from adhocracy4.comments_async import serializers as a4_serializers
from apps.contrib.dates import get_date_display
from apps.moderatorfeedback.models import ModeratorCommentStatement


class ModeratorCommentStatementSerializer(serializers.ModelSerializer):
    last_edit = serializers.SerializerMethodField()

    class Meta:
        model = ModeratorCommentStatement
        fields = ['last_edit', 'pk', 'statement']
        read_only_fields = ['last_edit', 'pk']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        validated_data['comment'] = self.context['view'].comment

        return super().create(validated_data)

    def update(self, statement, validated_data):
        validated_data['creator'] = self.context['request'].user

        return super().update(statement, validated_data)

    def get_last_edit(self, statement):
        if statement.modified:
            return get_date_display(statement.modified)
        else:
            return get_date_display(statement.created)


class CommentWithStatementSerializer(a4_serializers.CommentSerializer):

    moderator_statement = ModeratorCommentStatementSerializer(read_only=True)

    class Meta:
        model = Comment
        read_only_fields = \
            a4_serializers.CommentSerializer.Meta.read_only_fields + \
            ('moderator_comment_statement',)
        exclude = ('creator',)


class CommentWithStatementListSerializer(CommentWithStatementSerializer):
    """Serializer for the comments to be used when viewed as list."""


class ThreadSerializer(CommentWithStatementSerializer):
    """Serializes a comment including child comment (replies)."""

    child_comments = CommentWithStatementSerializer(many=True, read_only=True)


class ThreadListSerializer(CommentWithStatementListSerializer):
    """
    Serializes comments when viewed.

    As list including child comment (replies).
    """

    child_comments = CommentWithStatementListSerializer(many=True,
                                                        read_only=True)
