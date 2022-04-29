from rest_framework import serializers

from apps.classifications.models import AIClassification
from apps.classifications.models import UserClassification


class UserClassificationSerializer(serializers.ModelSerializer):
    classifications = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = UserClassification
        fields = ['classifications', 'comment_text',
                  'created', 'is_pending', 'pk', 'user_message']

    def get_classifications(self, instance):
        return instance.get_classifications_list()

    def get_created(self, instance):
        return instance.created.strftime('%d.%m.%y')


class AIClassificationSerializer(serializers.ModelSerializer):
    classifications = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = AIClassification
        fields = ['classifications', 'comment_text',
                  'created', 'is_pending', 'pk']

    def get_classifications(self, instance):
        return instance.get_classifications_list()

    def get_created(self, instance):
        return instance.created.strftime('%d.%m.%y')
