import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_filters(apiclient,
                 ai_classification_factory,
                 user_classification_factory,
                 comment_factory,
                 idea):
    comment_1 = comment_factory(content_object=idea)
    comment_2 = comment_factory(content_object=idea)
    comment_3 = comment_factory(content_object=idea)
    user_classification_factory(
        comment=comment_1)
    ai_classification_factory(
        comment=comment_1,
        classifications=['ENGAGING'],
        is_pending=False)
    ai_classification_factory(
        comment=comment_2)
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

    url_filter_archived = \
        url + '?has_pending_notifications=False&classification='
    response = apiclient.get(url_filter_archived)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['pk'] == comment_3.pk

    url_filter_pending = \
        url + '?has_pending_notifications=True&classification='
    response = apiclient.get(url_filter_pending)
    assert response.status_code == 200
    assert len(response.data) == 2

    url_filter_offensive = \
        url + '?has_pending_notifications=&classification=OFFENSIVE'
    response = apiclient.get(url_filter_offensive)
    assert response.status_code == 200
    assert len(response.data) == 3

    url_filter_engaging = \
        url + '?has_pending_notifications=&classification=ENGAGING'
    response = apiclient.get(url_filter_engaging)
    assert response.status_code == 200
    assert len(response.data) == 1

    url_filter_pending_engaging = \
        url + '?has_pending_notifications=True&classification=ENGAGING'
    response = apiclient.get(url_filter_pending_engaging)
    assert response.status_code == 200
    assert len(response.data) == 0

    url_filter_archived_engaging = \
        url + '?has_pending_notifications=False&classification=ENGAGING'
    response = apiclient.get(url_filter_archived_engaging)
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_ordering_filter(
        apiclient, ai_classification_factory, user_classification_factory,
        comment_factory, idea):
    comment_1 = comment_factory(content_object=idea)
    comment_2 = comment_factory(content_object=idea)
    comment_3 = comment_factory(content_object=idea)
    user_classification_factory(
        comment=comment_1,
        is_pending=False)
    ai_classification_factory(
        comment=comment_1,
        classifications=['ENGAGING'],
        is_pending=False)
    user_classification_factory(
        comment=comment_2)
    user_classification_factory(
        comment=comment_2)
    ai_classification_factory(
        comment=comment_2)
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
    assert response.data[0]['pk'] == comment_3.pk
    assert response.data[1]['pk'] == comment_2.pk
    assert response.data[2]['pk'] == comment_1.pk

    url_ordering = url + '?ordering=new'
    response = apiclient.get(url_ordering)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]['pk'] == comment_3.pk
    assert response.data[1]['pk'] == comment_2.pk
    assert response.data[2]['pk'] == comment_1.pk

    url_ordering_new = url + '?ordering=new'
    response = apiclient.get(url_ordering_new)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]['pk'] == comment_3.pk
    assert response.data[1]['pk'] == comment_2.pk
    assert response.data[2]['pk'] == comment_1.pk

    url_ordering_old = url + '?ordering=old'
    response = apiclient.get(url_ordering_old)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]['pk'] == comment_1.pk
    assert response.data[1]['pk'] == comment_2.pk
    assert response.data[2]['pk'] == comment_3.pk

    url_ordering_most = url + '?ordering=most'
    response = apiclient.get(url_ordering_most)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]['pk'] == comment_2.pk
    assert response.data[1]['pk'] == comment_1.pk
    assert response.data[2]['pk'] == comment_3.pk
