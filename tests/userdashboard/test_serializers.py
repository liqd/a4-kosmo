from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from apps.contrib import dates


@pytest.mark.django_db
def test_category_counts(apiclient,
                         ai_classification_factory,
                         user_classification_factory,
                         comment_factory,
                         idea):
    # comment with archived and pending classifications
    comment_1 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_1)
    ai_classification_factory(
        comment=comment_1,
        classifications=['OFFENSIVE', 'FACTCLAIMING'])
    ai_classification_factory(
        comment=comment_1,
        classifications=['OFFENSIVE', 'ENGAGING'],
        is_pending=False)

    # comment with only pending classifications
    comment_2 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_2)
    ai_classification_factory(
        comment=comment_2,
        classifications=['OFFENSIVE', 'FACTCLAIMING'])
    ai_classification_factory(
        comment=comment_2,
        classifications=['OFFENSIVE', 'ENGAGING'])

    # comment with only archived classifications
    comment_3 = comment_factory(content_object=idea)
    user_classification_factory(
        comment=comment_3,
        is_pending=False)
    ai_classification_factory(
        comment=comment_3,
        classifications=['OFFENSIVE', 'FACTCLAIMING'],
        is_pending=False)
    ai_classification_factory(
        comment=comment_3,
        classifications=['OFFENSIVE', 'ENGAGING'],
        is_pending=False)

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password='password')
    url = reverse('moderationcomments-list',
                  kwargs={'project_pk': project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    comment_1_data = [comment for comment in response.data
                      if comment['pk'] == comment_1.pk][0]
    comment_2_data = [comment for comment in response.data
                      if comment['pk'] == comment_2.pk][0]
    comment_3_data = [comment for comment in response.data
                      if comment['pk'] == comment_3.pk][0]
    assert comment_1_data['category_counts'] == {
        'offensive': 2,
        'fact claiming': 1,
        'AI': 1
    }
    assert comment_2_data['category_counts'] == \
           comment_3_data['category_counts'] == {
        'offensive': 3,
        'fact claiming': 1,
        'engaging': 1,
        'AI': 2
    }


@pytest.mark.django_db
def test_pending_and_archived_flags(apiclient,
                                    ai_classification_factory,
                                    user_classification_factory,
                                    comment_factory,
                                    idea):
    # comment with archived and pending classifications
    comment_1 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_1)
    ai_classification_factory(comment=comment_1)
    ai_classification_factory(
        comment=comment_1,
        is_pending=False)

    # comment with only pending classifications
    comment_2 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_2)
    ai_classification_factory(comment=comment_2)
    ai_classification_factory(comment=comment_2)

    # comment with only archived classifications
    comment_3 = comment_factory(content_object=idea)
    user_classification_factory(
        comment=comment_3,
        is_pending=False)
    ai_classification_factory(
        comment=comment_3,
        is_pending=False)
    ai_classification_factory(
        comment=comment_3,
        is_pending=False)

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password='password')
    url = reverse('moderationcomments-list',
                  kwargs={'project_pk': project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

    comment_1_data = [comment for comment in response.data
                      if comment['pk'] == comment_1.pk][0]
    comment_2_data = [comment for comment in response.data
                      if comment['pk'] == comment_2.pk][0]
    comment_3_data = [comment for comment in response.data
                      if comment['pk'] == comment_3.pk][0]
    assert comment_1_data['has_pending_and_archived_notifications']
    assert comment_1_data['has_pending_notifications']
    assert comment_1_data['num_active_notifications'] == 2
    assert not comment_2_data['has_pending_and_archived_notifications']
    assert comment_2_data['has_pending_notifications']
    assert comment_2_data['num_active_notifications'] == 3
    assert not comment_3_data['has_pending_and_archived_notifications']
    assert not comment_3_data['has_pending_notifications']
    assert comment_3_data['num_active_notifications'] == 3


@pytest.mark.django_db
def test_time_of_last_notification(apiclient,
                                   ai_classification_factory,
                                   user_classification_factory,
                                   comment_factory,
                                   idea):
    comment = comment_factory(content_object=idea)
    time_last_notification = parse('2022-01-01 17:00:00 UTC')
    user_classification_factory(
        comment=comment,
        created=time_last_notification - timedelta(hours=2))
    ai_classification_factory(
        comment=comment,
        created=time_last_notification - timedelta(hours=1))
    ai_classification_factory(
        comment=comment,
        created=time_last_notification)

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password='password')
    url = reverse('moderationcomments-list',
                  kwargs={'project_pk': project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['time_of_last_notification'] == \
           dates.get_date_display(time_last_notification)


@pytest.mark.django_db
def test_last_edit(apiclient,
                   ai_classification_factory,
                   user_classification_factory,
                   comment_factory,
                   idea):
    comment_1 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_1)
    comment_2 = comment_factory(content_object=idea)
    ai_classification_factory(comment=comment_2)

    with freeze_time(comment_2.created + timedelta(minutes=3)):
        comment_2.modified = timezone.now()
        comment_2.save()

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password='password')
    url = reverse('moderationcomments-list',
                  kwargs={'project_pk': project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    comment_1_data = [comment for comment in response.data
                      if comment['pk'] == comment_1.pk][0]
    comment_2_data = [comment for comment in response.data
                      if comment['pk'] == comment_2.pk][0]

    assert not comment_1_data['is_modified']
    assert comment_1_data['last_edit'] == \
           dates.get_date_display(comment_1.created)
    assert comment_2_data['is_modified']
    assert comment_2_data['last_edit'] == \
           dates.get_date_display(comment_2.modified)
