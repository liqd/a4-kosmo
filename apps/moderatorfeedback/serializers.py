from django.template import defaultfilters
from django.utils import timezone
from rest_framework import serializers

from adhocracy4.comments.models import Comment
from adhocracy4.comments_async import serializers as a4_serializers
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
        last_edit = statement.created
        if statement.modified:
            last_edit = statement.modified

        localtime_created = timezone.localtime(last_edit)
        last_edit_date = defaultfilters.date(localtime_created)
        last_edit_time = defaultfilters.time(localtime_created)
        return last_edit_date + ', ' + last_edit_time


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
