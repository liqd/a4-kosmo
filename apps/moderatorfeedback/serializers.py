from rest_framework import serializers

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
            return statement.modified
        return statement.created
