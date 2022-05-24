from rest_framework import serializers

from apps.classifications.models import AIClassification
from apps.classifications.models import UserClassification


class UserClassificationSerializer(serializers.ModelSerializer):
    classification = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = UserClassification
        fields = ['classification', 'comment_text',
                  'created', 'is_pending', 'pk', 'user_message']

    def get_classification(self, instance):
        return instance.get_classification_display()

    def get_created(self, instance):
        return instance.created.strftime('%d.%m.%y')


class AIClassificationSerializer(serializers.ModelSerializer):
    classification = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = AIClassification
        fields = ['classification', 'comment_text',
                  'created', 'is_pending', 'pk']

    def get_classification(self, instance):
        return instance.get_classification_display()

    def get_created(self, instance):
        return instance.created.strftime('%d.%m.%y')
