import pytest
from django.db.models import signals

from adhocracy4.comments.models import Comment
from apps.classifications.signals import get_ai_classification


@pytest.mark.django_db
def test_post_save_comment_signal_sent_on_comment_text_change(idea,
                                                              comment_factory,
                                                              caplog):
    assert(get_ai_classification in signals.post_save._live_receivers(Comment))
    comment = comment_factory(content_object=idea,
                              comment='lala')
    assert len(caplog.records) == 1
    assert('No ai api auth token provided.' in str(caplog.records[-1]))

    comment.comment = 'modified comment'
    comment.save()
    assert len(caplog.records) == 2

    comment.is_blocked = True
    comment.save()
    assert len(caplog.records) == 2
