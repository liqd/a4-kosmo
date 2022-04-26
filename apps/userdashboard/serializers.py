from django.template import defaultfilters
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.hashable import make_hashable
from django.utils.translation import gettext as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.comments.models import Comment
from apps.classifications.models import CLASSIFICATION_CHOICES
from apps.moderatorfeedback.serializers import \
    ModeratorCommentStatementSerializer


class ModerationCommentSerializer(serializers.ModelSerializer):

    category_counts = serializers.SerializerMethodField()
    comment_url = serializers.SerializerMethodField()
    has_pending_notifications = serializers.SerializerMethodField()
    has_pending_and_archived_notifications = \
        serializers.SerializerMethodField()
    is_modified = serializers.SerializerMethodField()
    last_edit = serializers.SerializerMethodField()
    moderator_statement = ModeratorCommentStatementSerializer(read_only=True)
    num_active_notifications = serializers.SerializerMethodField()
    time_of_last_notification = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    user_profile_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['category_counts', 'comment', 'comment_url',
                  'has_pending_and_archived_notifications',
                  'has_pending_notifications', 'is_blocked',
                  'is_moderator_marked', 'is_modified', 'last_edit',
                  'moderator_statement', 'num_active_notifications',
                  'pk', 'time_of_last_notification', 'user_image', 'user_name',
                  'user_profile_url']

    def get_has_pending_and_archived_notifications(self, comment):
        """Return if comment has both pending and archived notifications.

        False if only archived or pending notifications exist.
        """
        num_all_notificiations = self._get_num_all_notifications(comment)
        num_pending_notifications = \
            self._get_num_pending_notifications(comment)

        return num_all_notificiations > num_pending_notifications > 0

    def get_category_counts(self, comment):
        """Return counts of each category as dictionary.

        If there are both pending and archived classifications for the comment,
        only consider the pending ones.
        """
        if self.get_has_pending_and_archived_notifications(comment):
            ai_classifications = comment.ai_classifications.filter(
                is_pending=True)
            user_classifications = comment.user_classifications.filter(
                is_pending=True)
        else:
            ai_classifications = comment.ai_classifications.all()
            user_classifications = comment.user_classifications.all()
        ai_classifications_lists = \
            list(ai_classifications.values_list('classifications', flat=True))
        ai_list = [classification for sublist in ai_classifications_lists
                   for classification in sublist]
        user_classifications_lists = \
            list(user_classifications.values_list('classifications',
                                                  flat=True))
        user_list = [classification for sublist in user_classifications_lists
                     for classification in sublist]
        classifications_list = ai_list + user_list
        # serialize translated classifications as keys
        choices_dict = dict(make_hashable(CLASSIFICATION_CHOICES))
        category_counts = {force_str(choices_dict[classification]):
                           classifications_list.count(classification)
                           for classification in classifications_list}

        num_ai_classifications = ai_classifications.count()
        if num_ai_classifications > 0:
            category_counts[_('AI')] = num_ai_classifications

        return category_counts

    def get_comment_url(self, instance):
        return instance.get_absolute_url()

    def _get_date_display(self, date):
        local_date = timezone.localtime(date)
        return '{}, {}'.format(defaultfilters.date(local_date),
                               defaultfilters.time(local_date))

    def get_is_modified(self, comment):
        return comment.modified is not None

    def get_last_edit(self, comment):
        if comment.modified:
            return self._get_date_display(comment.modified)
        else:
            return self._get_date_display(comment.created)

    def get_time_of_last_notification(self, comment):
        ai_dates = comment.ai_classifications.all().values_list(
            'created', flat=True)
        user_dates = comment.user_classifications.all().values_list(
            'created', flat=True)

        return self._get_date_display(max(ai_dates.union(user_dates)))

    def get_user_name(self, comment):
        if comment.is_censored or comment.is_removed:
            return _('unknown user')
        return str(comment.creator.username)

    def get_user_image_fallback(self, comment):
        """Load small thumbnail images for default user images."""
        if (comment.is_censored or comment.is_removed):
            return None
        try:
            if comment.creator.avatar_fallback:
                return comment.creator.avatar_fallback
        except AttributeError:
            pass
        return None

    def get_user_image(self, comment):
        """Load small thumbnail images for user images."""
        if (comment.is_censored or comment.is_removed):
            return None
        try:
            if comment.creator.avatar:
                avatar = get_thumbnailer(comment.creator.avatar)['avatar']
                return avatar.url
        except AttributeError:
            pass
        return self.get_user_image_fallback(comment)

    def get_user_profile_url(self, comment):
        if comment.is_censored or comment.is_removed:
            return ''
        try:
            return comment.creator.get_absolute_url()
        except AttributeError:
            return ''

    def _get_num_all_notifications(self, comment):
        num_ai_classifications = comment.ai_classifications.all().count()
        num_user_classifications = comment.user_classifications.all().count()
        return num_ai_classifications + num_user_classifications

    def _get_num_pending_notifications(self, comment):
        num_pending_ai_classifications = comment.ai_classifications.\
            all().filter(is_pending=True).count()
        num_pending_user_classifications = comment.user_classifications.\
            all().filter(is_pending=True).count()

        return (num_pending_ai_classifications +
                num_pending_user_classifications)

    def get_has_pending_notifications(self, comment):
        return self._get_num_pending_notifications(comment) > 0

    def get_num_active_notifications(self, comment):
        """Return number of either all classifications or only pending ones.

        If there are both pending and archived classifications for the comment,
        only return number of pending ones, else number of all
        classifications (pending and archived).
        """
        if self.get_has_pending_and_archived_notifications(comment):
            return self._get_num_pending_notifications(comment)
        else:
            return self._get_num_all_notifications(comment)
