import pytest
from django.urls import reverse

from apps.moderatorfeedback.models import ModeratorCommentStatement


@pytest.mark.django_db
def test_anonymous_cannot_add_statement(apiclient, idea, comment_factory):
    comment = comment_factory(pk=1, content_object=idea)

    assert ModeratorCommentStatement.objects.all().count() == 0
    url = reverse('moderatorstatement-list', kwargs={'comment_pk': comment.pk})
    data = {'statement': 'a statement'}
    response = apiclient.post(url, data)
    assert response.status_code == 403
    assert ModeratorCommentStatement.objects.all().count() == 0


@pytest.mark.django_db
def test_user_cannot_add_statement(apiclient, idea, user, comment_factory):
    comment = comment_factory(pk=1, content_object=idea)

    assert ModeratorCommentStatement.objects.all().count() == 0
    url = reverse('moderatorstatement-list', kwargs={'comment_pk': comment.pk})
    data = {'statement': 'a statement'}
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data)
    assert response.status_code == 403
    assert ModeratorCommentStatement.objects.all().count() == 0


@pytest.mark.django_db
def test_moderator_can_add_statement(apiclient, idea, user, comment_factory):
    comment = comment_factory(pk=1, content_object=idea)
    idea.project.moderators.add(user)

    assert ModeratorCommentStatement.objects.all().count() == 0
    url = reverse('moderatorstatement-list', kwargs={'comment_pk': comment.pk})
    data = {'statement': 'a statement'}
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data)
    assert response.status_code == 201
    assert ModeratorCommentStatement.objects.all().count() == 1


@pytest.mark.django_db
def test_initiator_can_add_statement(apiclient, idea, user, comment_factory):
    comment = comment_factory(pk=1, content_object=idea)
    idea.project.organisation.initiators.add(user)

    assert ModeratorCommentStatement.objects.all().count() == 0
    url = reverse('moderatorstatement-list', kwargs={'comment_pk': comment.pk})
    data = {'statement': 'a statement'}
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data)
    assert response.status_code == 201
    assert ModeratorCommentStatement.objects.all().count() == 1


@pytest.mark.django_db
def test_admin_can_add_statement(admin, apiclient, idea, comment_factory):
    comment = comment_factory(pk=1, content_object=idea)

    assert ModeratorCommentStatement.objects.all().count() == 0
    url = reverse('moderatorstatement-list', kwargs={'comment_pk': comment.pk})
    data = {'statement': 'a statement'}
    apiclient.force_authenticate(user=admin)
    response = apiclient.post(url, data)
    assert response.status_code == 201
    assert ModeratorCommentStatement.objects.all().count() == 1


@pytest.mark.django_db
def test_user_cannot_edit_statement(apiclient, idea, user, comment_factory,
                                    moderator_comment_statement_factory):
    comment = comment_factory(content_object=idea)
    statement = moderator_comment_statement_factory(comment=comment)
    assert ModeratorCommentStatement.objects.all().count() == 1
    url = reverse('moderatorstatement-detail',
                  kwargs={
                      'comment_pk': statement.comment.pk,
                      'pk': statement.pk,
                  })
    data = {'statement': 'a changed statement'}
    apiclient.force_authenticate(user=user)
    response = apiclient.put(url, data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db
def test_moderator_can_edit_statement(apiclient, idea, user, comment_factory,
                                      moderator_comment_statement_factory):
    idea.project.moderators.add(user)
    comment = comment_factory(content_object=idea)
    statement = moderator_comment_statement_factory(comment=comment)
    assert ModeratorCommentStatement.objects.all().count() == 1
    url = reverse('moderatorstatement-detail',
                  kwargs={
                      'comment_pk': statement.comment.pk,
                      'pk': statement.pk,
                  })
    data = {'statement': 'a changed statement'}
    apiclient.force_authenticate(user=user)
    response = apiclient.put(url, data, format='json')
    assert response.status_code == 200
    assert ModeratorCommentStatement.objects.all().count() == 1
    assert ModeratorCommentStatement.objects.first().statement \
           == 'a changed statement'


@pytest.mark.django_db
def test_user_cannot_delete_statement(apiclient, idea, user, comment_factory,
                                      moderator_comment_statement_factory):
    comment = comment_factory(content_object=idea)
    statement = moderator_comment_statement_factory(comment=comment)
    assert ModeratorCommentStatement.objects.all().count() == 1
    url = reverse('moderatorstatement-detail',
                  kwargs={
                      'comment_pk': statement.comment.pk,
                      'pk': statement.pk,
                  })
    apiclient.force_authenticate(user=user)
    response = apiclient.delete(url)
    assert response.status_code == 403
    assert ModeratorCommentStatement.objects.all().count() == 1


@pytest.mark.django_db
def test_moderator_can_delete_statement(apiclient, idea, user, comment_factory,
                                        moderator_comment_statement_factory):
    idea.project.moderators.add(user)
    comment = comment_factory(content_object=idea)
    statement = moderator_comment_statement_factory(comment=comment)
    assert ModeratorCommentStatement.objects.all().count() == 1
    url = reverse('moderatorstatement-detail',
                  kwargs={
                      'comment_pk': statement.comment.pk,
                      'pk': statement.pk,
                  })
    apiclient.force_authenticate(user=user)
    response = apiclient.delete(url)
    assert response.status_code == 204
    assert ModeratorCommentStatement.objects.all().count() == 0
