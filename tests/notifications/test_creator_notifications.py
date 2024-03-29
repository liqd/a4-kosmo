import pytest
from django.core import mail
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_notify_creator(idea, comment_factory):
    """Check if creators get emails on comment create."""
    creator = idea.creator
    comment = comment_factory(content_object=idea)

    # 3 emails because of moderator notifications for idea and comment
    assert len(mail.outbox) == 3
    assert mail.outbox[1].to[0] == creator.email
    assert mail.outbox[1].subject.startswith("Reaction to your contribution")

    comment_creator = comment.creator
    comment_factory(content_object=comment)

    # 2 more emails because of moderator notification
    assert len(mail.outbox) == 5
    assert mail.outbox[3].to[0] == comment_creator.email
    assert mail.outbox[3].subject.startswith("Reaction to your contribution")


@pytest.mark.django_db
def test_notify_creator_exclude_moderator(idea, comment_factory, user):
    """Check if moderators are excluded from creator notifications."""
    creator_moderator = idea.creator
    idea.project.moderators.add(creator_moderator)
    comment_factory(content_object=idea)

    assert len(mail.outbox) == 3
    # moderator notification instead of creator notification
    assert mail.outbox[1].to[0] == creator_moderator.email
    assert not mail.outbox[1].subject.startswith("Reaction to your contribution")
    assert mail.outbox[1].subject.startswith("A comment was added to the project")


@pytest.mark.django_db
def test_notify_creator_exclude_own_comment(idea, comment_factory):
    """Check if creators does not get email on own comment create."""
    creator = idea.creator
    comment_factory(content_object=idea, creator=creator)

    # 2 emails because of moderator notifications for idea and comment
    assert len(mail.outbox) == 2


@pytest.mark.django_db
def test_notify_creator_on_moderator_feedback(proposal_factory, client):
    """Check if creator gets emails on moderator feedback."""
    proposal = proposal_factory()
    # moderator notifications for proposal
    assert len(mail.outbox) == 1

    creator = proposal.creator
    project = proposal.project
    moderator = project.moderators.first()

    url = reverse(
        "a4_candy_budgeting:proposal-moderate",
        kwargs={
            "organisation_slug": project.organisation.slug,
            "pk": proposal.pk,
            "year": proposal.created.year,
        },
    )
    client.login(username=moderator.email, password="password")

    data = {
        "moderator_status": "test",
        "is_archived": False,
        "feedback_text": "its a feedback text",
    }
    response = client.post(url, data)
    assert redirect_target(response) == "proposal-detail"

    # 2nd email about moderator feedback
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to[0] == creator.email
    assert mail.outbox[1].subject.startswith("Feedback for your contribution")


@pytest.mark.django_db
def test_notify_comment_creator_on_block(
    idea, comment_factory, apiclient, ai_classification_factory
):
    """Check if creator gets email on comment blocked."""
    comment = comment_factory(content_object=idea)
    ai_classification_factory(comment=comment)
    creator = comment.creator
    moderator = comment.project.moderators.first()

    # 3 emails because of creator notification for reaction on idea
    assert len(mail.outbox) == 3

    url = reverse(
        "moderationcomments-detail",
        kwargs={
            "project_pk": comment.project.pk,
            "pk": comment.pk,
        },
    )
    data = {
        "is_blocked": True,
    }

    apiclient.force_authenticate(user=moderator)
    response = apiclient.patch(url, data, format="json")
    assert response.status_code == 200
    assert len(mail.outbox) == 4
    assert mail.outbox[3].to[0] == creator.email
    assert mail.outbox[3].subject.startswith("Your contribution was deleted")


@pytest.mark.django_db
def test_no_notify_comment_creator_on_unblock(
    idea, comment_factory, apiclient, ai_classification_factory
):
    """Check creator gets no email on comment unblocked."""
    comment = comment_factory(content_object=idea, is_blocked=True)
    ai_classification_factory(comment=comment)
    moderator = comment.project.moderators.first()

    # 3 emails because of creator notification for reaction on idea
    assert len(mail.outbox) == 3

    url = reverse(
        "moderationcomments-detail",
        kwargs={
            "project_pk": comment.project.pk,
            "pk": comment.pk,
        },
    )
    data = {
        "is_blocked": False,
    }

    apiclient.force_authenticate(user=moderator)
    response = apiclient.patch(url, data, format="json")
    assert response.status_code == 200
    assert len(mail.outbox) == 3


@pytest.mark.django_db
def test_notify_comment_creator_on_feedback(
    idea, comment_factory, moderator_comment_feedback_factory
):
    """Check if creator gets email on comment feedback added."""
    comment = comment_factory(content_object=idea)
    creator = comment.creator

    # 3 emails because of creator notification for reaction on idea
    assert len(mail.outbox) == 3

    moderator_comment_feedback_factory(comment=comment)

    assert len(mail.outbox) == 4
    assert mail.outbox[3].to[0] == creator.email
    assert mail.outbox[3].subject.startswith("Feedback of the moderation")
