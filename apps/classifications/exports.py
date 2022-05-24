from django.utils import timezone
from django.views.generic.list import MultipleObjectMixin
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.exports import mixins
from adhocracy4.exports import views

from . import models


class AbstractClassificationExport(PermissionRequiredMixin,
                                   mixins.ExportModelFieldsMixin,
                                   views.BaseExport,
                                   MultipleObjectMixin,
                                   views.AbstractXlsxExportView):

    fields = ['id', 'created', 'classification', 'comment_text', 'is_pending',
              'comment']
    related_fields = {'comment': ['id', 'comment', 'is_blocked',
                                  'is_moderator_marked', 'created',
                                  'modified', 'moderator_statement']}
    ordering = 'comment__pk'

    def get_object_list(self):
        return self.get_queryset().all()

    def has_permission(self):
        return self.request.user.is_superuser


class AIClassificationExport(AbstractClassificationExport):
    model = models.AIClassification

    def get_base_filename(self):
        return '%s_%s' % ('ai-classifications',
                          timezone.now().strftime('%Y%m%dT%H%M%S'))


class UserClassificationExport(AbstractClassificationExport):

    model = models.UserClassification

    def __init__(self):
        self.fields.append('user_message')

    def get_base_filename(self):
        return '%s_%s' % ('user-classifications',
                          timezone.now().strftime('%Y%m%dT%H%M%S'))
