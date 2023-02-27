from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.comments.models import Comment
from adhocracy4.models import base

CLASSIFICATION_CHOICES = (
    # Translators: kosmo
    ('OFFENSIVE', _('offensive')),
    # Translators: kosmo
    ('ENGAGING', _('engaging')),
    # Translators: kosmo
    ('FACTCLAIMING', _('fact claiming')),
    # Translators: kosmo
    ('OTHER', _('other')),
)


class Classification(models.Model):

    class Meta:
        abstract = True

    is_pending = models.BooleanField(default=True)

    classification = models.CharField(max_length=50,
                                      choices=CLASSIFICATION_CHOICES)

    comment_text = models.TextField(max_length=4000)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.comment_text = self.comment.comment
        super().save(*args, **kwargs)

    @property
    def project(self):
        return self.comment.module.project


class UserClassification(Classification, base.UserGeneratedContentModel):

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='user_classifications'
    )

    user_message = models.TextField(max_length=1024)


class AIClassification(Classification, base.TimeStampedModel):

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='ai_classifications'
    )
