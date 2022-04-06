from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.comments.models import Comment
from apps.classifications.models import AIClassification
from apps.classifications.models import UserClassification


class CommentSerializer(serializers.ModelSerializer):

    comment_url = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    user_profile_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['comment_url', 'user_name', 'user_image', 'user_profile_url',
                  'is_blocked']

    def get_comment_url(self, instance):
        return instance.get_absolute_url()

    def get_user_name(self, instance):
        if instance.is_censored or instance.is_removed:
            return _('unknown user')
        return str(instance.creator.username)

    def get_user_image_fallback(self, obj):
        """Load small thumbnail images for default user images."""
        if(obj.is_censored or obj.is_removed):
            return None
        try:
            if obj.creator.avatar_fallback:
                return obj.creator.avatar_fallback
        except AttributeError:
            pass
        return None

    def get_user_image(self, obj):
        """Load small thumbnail images for user images."""
        if(obj.is_censored or obj.is_removed):
            return None
        try:
            if obj.creator.avatar:
                avatar = get_thumbnailer(obj.creator.avatar)['avatar']
                return avatar.url
        except AttributeError:
            pass
        return self.get_user_image_fallback(obj)

    def get_user_profile_url(self, obj):
        if obj.is_censored or obj.is_removed:
            return ''
        try:
            return obj.creator.get_absolute_url()
        except AttributeError:
            return ''


class UserClassificationSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)
    classifications = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = UserClassification
        fields = ['api_url', 'classifications', 'comment', 'comment_text',
                  'created', 'is_pending', 'user_message']

    def get_classifications(self, instance):
        return instance.get_classifications_list()

    def get_created(self, instance):
        return instance.created.strftime('%d.%m.%y')

    def get_api_url(self, instance):
        return reverse('userclassifications-detail',
                       kwargs={'project_pk': instance.project.pk,
                               'pk': instance.pk})


class AIClassificationSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)
    classifications = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = AIClassification
        fields = ['api_url', 'classifications', 'comment', 'comment_text',
                  'created', 'is_pending']

    def get_classifications(self, instance):
        return instance.get_classifications_list()

    def get_created(self, instance):
        return instance.created.strftime('%d.%m.%y')

    def get_api_url(self, instance):
        return reverse('aiclassifications-detail',
                       kwargs={'project_pk': instance.project.pk,
                               'pk': instance.pk})
