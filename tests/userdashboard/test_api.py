import pytest
from dateutil.parser import parse
from django.urls import reverse


@pytest.mark.django_db
def test_anonymous_cannot_view_moderation_comments(apiclient, project):
    url = reverse('moderationcomments-list',
                  kwargs={'project_pk': project.pk})
    response = apiclient.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_wrong_moderator_cannot_view_moderation_comments(apiclient,
                                                         project_factory):
    project_1 = project_factory()
    project_2 = project_factory()

    moderator = project_1.moderators.first()
    apiclient.login(username=moderator.email, password='password')

    url = reverse('moderationcomments-list',
                  kwargs={'project_pk': project_2.pk})
    response = apiclient.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_view_moderation_comments(apiclient,
                                                ai_classification_factory,
                                                user_classification_factory,
                                                comment_factory,
                                                idea):
    comment_1 = comment_factory(content_object=idea)
    comment_2 = comment_factory(content_object=idea)
    user_classification_factory(
        comment=comment_1,
        created=parse('2022-01-01 17:00:00 UTC'))
    ai_classification_factory(
        comment=comment_2,
        created=parse('2022-01-01 18:00:00 UTC'))
    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password='password')

    url = reverse('moderationcomments-list',
                  kwargs={'project_pk': project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert comment_1.pk in response.data[1].values()
    assert comment_2.pk in response.data[0].values()


@pytest.mark.django_db
def test_moderator_can_block_and_highlight_comment(apiclient,
                                                   ai_classification_factory,
                                                   user_classification_factory,
                                                   comment_factory,
                                                   idea):
    comment_1 = comment_factory(content_object=idea)
    comment_2 = comment_factory(content_object=idea)
    user_classification_factory(
        comment=comment_1,
        created=parse('2022-01-01 17:00:00 UTC'))
    ai_classification_factory(
        comment=comment_2,
        created=parse('2022-01-01 18:00:00 UTC'))
    project = idea.project
    moderator = project.moderators.first()
    assert not comment_1.is_blocked
    assert not comment_2.is_moderator_marked

    apiclient.login(username=moderator.email, password='password')

    url_comment_1 = reverse('moderationcomments-detail',
                            kwargs={'project_pk': project.pk,
                                    'pk': comment_1.pk})
    data = {'is_blocked': True}
    response = apiclient.patch(url_comment_1, data, format='json')
    assert response.status_code == 200

    url_comment_2 = reverse('moderationcomments-detail',
                            kwargs={'project_pk': project.pk,
                                    'pk': comment_2.pk})
    data = {'is_moderator_marked': True}
    response = apiclient.patch(url_comment_2, data, format='json')
    assert response.status_code == 200

    comment_1.refresh_from_db()
    comment_2.refresh_from_db()
    assert comment_1.is_blocked
    assert comment_2.is_moderator_marked


@pytest.mark.django_db
def test_moderator_can_archive_classifications(apiclient,
                                               ai_classification_factory,
                                               user_classification_factory,
                                               comment_factory,
                                               idea):
    comment = comment_factory(content_object=idea)
    user_classification = user_classification_factory(
        comment=comment)
    ai_classification = ai_classification_factory(
        comment=comment)
    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password='password')

    url = reverse('moderationcomments-detail',
                  kwargs={'project_pk': project.pk,
                          'pk': comment.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert user_classification.is_pending
    assert ai_classification.is_pending
    assert response.data['has_pending_notifications']

    url_archive = url + 'archive/'
    response = apiclient.get(url_archive)
    assert response.status_code == 200
    user_classification.refresh_from_db()
    ai_classification.refresh_from_db()
    assert not user_classification.is_pending
    assert not ai_classification.is_pending
    assert not response.data['has_pending_notifications']

    url_unarchive = url + 'unarchive/'
    response = apiclient.get(url_unarchive)
    assert response.status_code == 200
    user_classification.refresh_from_db()
    ai_classification.refresh_from_db()
    assert user_classification.is_pending
    assert ai_classification.is_pending
    assert response.data['has_pending_notifications']


@pytest.mark.django_db
def test_moderator_can_view_classifications(apiclient,
                                            ai_classification_factory,
                                            user_classification_factory,
                                            comment_factory,
                                            idea):
    comment = comment_factory(content_object=idea)
    user_classification = user_classification_factory(
        comment=comment)
    ai_classification = ai_classification_factory(
        comment=comment)
    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password='password')

    url = reverse('moderationcomments-detail',
                  kwargs={'project_pk': project.pk,
                          'pk': comment.pk})

    url_ai_classifications = url + 'aiclassifications/'
    response = apiclient.get(url_ai_classifications)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert ai_classification.pk == response.data[0]['pk']

    url_user_classifications = url + 'userclassifications/'
    response = apiclient.get(url_user_classifications)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert user_classification.pk == response.data[0]['pk']


@pytest.mark.django_db
def test_queryset(apiclient,
                  ai_classification_factory,
                  user_classification_factory,
                  comment_factory,
                  idea_factory):
    idea = idea_factory(module__project__pk=1)
    other_idea = idea_factory(module__project__pk=2)
    project = idea.project

    comment_1 = comment_factory(content_object=idea)
    comment_2 = comment_factory(content_object=idea)
    comment_3 = comment_factory(content_object=idea)
    comment_4 = comment_factory(content_object=idea)
    comment_5 = comment_factory(content_object=other_idea)

    # comment_1 with 2 classifications, 1 pending
    user_classification_factory(comment=comment_1)
    ai_classification_factory(comment=comment_1, is_pending=False)
    # comment_2 with 1 pending classification
    ai_classification_factory(comment=comment_2)
    # comment_3 with 1 archived classification
    ai_classification_factory(comment=comment_3, is_pending=False)
    # comment_4 with no classifications
    # comment_5 in other project with 1 pending classification
    ai_classification_factory(comment=comment_5)

    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password='password')

    url = reverse('moderationcomments-list',
                  kwargs={'project_pk': project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    comment_pks = [comment['pk'] for comment in response.data]
    assert comment_1.pk in comment_pks
    assert comment_2.pk in comment_pks
    assert comment_3.pk in comment_pks
    assert comment_4.pk not in comment_pks
    assert comment_5.pk not in comment_pks
