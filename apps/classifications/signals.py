import logging

import backoff
import httpx
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver

from adhocracy4.comments.models import Comment

from .models import AIClassification

client = httpx.Client()
logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=Comment)
def get_ai_classification(sender, instance, created, update_fields, **kwargs):
    comment_text_changed = \
        (getattr(instance, '_former_comment') != getattr(instance, 'comment'))
    if created or comment_text_changed:
        if hasattr(settings, 'AI_USAGE') and settings.AI_USAGE:
            if hasattr(settings, 'AI_API_AUTH_TOKEN') and \
                    settings.AI_API_AUTH_TOKEN:
                if hasattr(settings, 'AI_API_VERSION') and \
                        settings.AI_API_VERSION:
                    ai_api_version = settings.AI_API_VERSION
                else:
                    ai_api_version = '3.0'
                try:
                    response = call_ai_api(comment=instance,
                                           version=ai_api_version)
                    if response.status_code == 200:
                        extract_and_save_ai_classifications(
                            comment=instance,
                            classifications=response.json()['classification'],
                            version=ai_api_version)
                except httpx.HTTPError as e:
                    logger.error('Error connecting to %s: %s',
                                 settings.AI_API_URL, str(e))
            else:
                logger.error('No ai api auth token provided. '
                             'Disable ai usage or provide token.')


def skip_retry(e):
    if isinstance(e, httpx.HTTPStatusError):
        return 400 <= e.response.status_code < 500
    return False


@backoff.on_exception(backoff.expo,
                      httpx.HTTPError,
                      max_tries=4,
                      factor=2,
                      giveup=skip_retry)
def call_ai_api(comment, version):
    response = client.post(settings.AI_API_URL,
                           data={'comment': comment.comment},
                           headers={'Authorization': 'Token {}'.format(
                                    settings.AI_API_AUTH_TOKEN),
                                    'Accept': 'application/json; '
                                              'version={}'.format(
                                    version)
                                    }
                           )
    response.raise_for_status()

    return response


def extract_and_save_ai_classifications(comment, classifications, version):
    # version 2
    if version == '2.0' and classifications == 'OFFENSE':
        classification = AIClassification(
            comment=comment,
            classification='OFFENSIVE'
        )
        classification.save()
    # version 3
    elif version == '3.0' and 1 in classifications.values():
        detected_classifications = [c for c in classifications
                                    if classifications[c] == 1]
        for classification in detected_classifications:
            classification = AIClassification(
                comment=comment,
                classification=classification
            )
            classification.save()
