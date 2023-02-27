from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from apps.contrib import dates


@pytest.mark.django_db
def test_category_counts(
    apiclient,
    ai_classification_factory,
    user_classification_factory,
    comment_factory,
    idea,
):
    # comment with archived and pending classifications
    comment_1 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_1)
    ai_classification_factory(comment=comment_1, classification="OFFENSIVE")
    ai_classification_factory(comment=comment_1, classification="FACTCLAIMING")
    ai_classification_factory(
        comment=comment_1, classification="OFFENSIVE", is_pending=False
    )
    ai_classification_factory(
        comment=comment_1, classification="ENGAGING", is_pending=False
    )

    # comment with only pending classifications
    comment_2 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_2)
    ai_classification_factory(comment=comment_2, classification="OFFENSIVE")
    ai_classification_factory(comment=comment_2, classification="FACTCLAIMING")
    ai_classification_factory(comment=comment_2, classification="OFFENSIVE")
    ai_classification_factory(comment=comment_2, classification="ENGAGING")

    # comment with only archived classifications
    comment_3 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_3, is_pending=False)
    ai_classification_factory(
        comment=comment_3, classification="OFFENSIVE", is_pending=False
    )
    ai_classification_factory(
        comment=comment_3, classification="FACTCLAIMING", is_pending=False
    )
    ai_classification_factory(
        comment=comment_3, classification="OFFENSIVE", is_pending=False
    )
    ai_classification_factory(
        comment=comment_3, classification="ENGAGING", is_pending=False
    )

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password="password")
    url = reverse("moderationcomments-list", kwargs={"project_pk": project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    comment_1_data = [
        comment for comment in response.data if comment["pk"] == comment_1.pk
    ][0]
    comment_2_data = [
        comment for comment in response.data if comment["pk"] == comment_2.pk
    ][0]
    comment_3_data = [
        comment for comment in response.data if comment["pk"] == comment_3.pk
    ][0]
    assert comment_1_data["category_counts"] == {
        "offensive": {"count": 2, "translated": "offensive"},
        "factclaiming": {"count": 1, "translated": "fact claiming"},
    }
    assert (
        comment_2_data["category_counts"]
        == comment_3_data["category_counts"]
        == {
            "offensive": {"count": 3, "translated": "offensive"},
            "factclaiming": {"count": 1, "translated": "fact claiming"},
            "engaging": {"count": 1, "translated": "engaging"},
        }
    )


@pytest.mark.django_db
def test_pending_and_archived_flags(
    apiclient,
    ai_classification_factory,
    user_classification_factory,
    comment_factory,
    idea,
):
    # comment with archived and pending classifications
    comment_1 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_1)
    ai_classification_factory(comment=comment_1)
    ai_classification_factory(comment=comment_1, is_pending=False)

    # comment with only pending classifications
    comment_2 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_2)
    ai_classification_factory(comment=comment_2)
    ai_classification_factory(comment=comment_2)

    # comment with only archived classifications
    comment_3 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_3, is_pending=False)
    ai_classification_factory(comment=comment_3, is_pending=False)
    ai_classification_factory(comment=comment_3, is_pending=False)

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password="password")
    url = reverse("moderationcomments-list", kwargs={"project_pk": project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

    comment_1_data = [
        comment for comment in response.data if comment["pk"] == comment_1.pk
    ][0]
    comment_2_data = [
        comment for comment in response.data if comment["pk"] == comment_2.pk
    ][0]
    comment_3_data = [
        comment for comment in response.data if comment["pk"] == comment_3.pk
    ][0]
    assert comment_1_data["has_pending_and_archived_notifications"]
    assert comment_1_data["has_pending_notifications"]
    assert comment_1_data["num_active_notifications"] == 2
    assert not comment_2_data["has_pending_and_archived_notifications"]
    assert comment_2_data["has_pending_notifications"]
    assert comment_2_data["num_active_notifications"] == 3
    assert not comment_3_data["has_pending_and_archived_notifications"]
    assert not comment_3_data["has_pending_notifications"]
    assert comment_3_data["num_active_notifications"] == 3


@pytest.mark.django_db
def test_time_of_last_notification(
    apiclient,
    ai_classification_factory,
    user_classification_factory,
    comment_factory,
    idea,
):
    comment = comment_factory(content_object=idea)
    time_last_notification = parse("2022-01-01 17:00:00 UTC")
    user_classification_factory(
        comment=comment, created=time_last_notification - timedelta(hours=2)
    )
    ai_classification_factory(
        comment=comment, created=time_last_notification - timedelta(hours=1)
    )
    ai_classification_factory(comment=comment, created=time_last_notification)

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password="password")
    url = reverse("moderationcomments-list", kwargs={"project_pk": project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["time_of_last_notification"] == dates.get_date_display(
        time_last_notification
    )


@pytest.mark.django_db
def test_last_edit(
    apiclient,
    ai_classification_factory,
    user_classification_factory,
    comment_factory,
    idea,
):
    comment_1 = comment_factory(content_object=idea)
    user_classification_factory(comment=comment_1)
    comment_2 = comment_factory(content_object=idea)
    ai_classification_factory(comment=comment_2)

    with freeze_time(comment_2.created + timedelta(minutes=3)):
        comment_2.modified = timezone.now()
        comment_2.save()

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password="password")
    url = reverse("moderationcomments-list", kwargs={"project_pk": project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    comment_1_data = [
        comment for comment in response.data if comment["pk"] == comment_1.pk
    ][0]
    comment_2_data = [
        comment for comment in response.data if comment["pk"] == comment_2.pk
    ][0]

    assert not comment_1_data["is_modified"]
    assert comment_1_data["last_edit"] == dates.get_date_display(comment_1.created)
    assert comment_2_data["is_modified"]
    assert comment_2_data["last_edit"] == dates.get_date_display(comment_2.modified)


@pytest.mark.django_db
def test_fields(
    apiclient,
    ai_classification_factory,
    user_classification_factory,
    comment_factory,
    idea,
    moderator_comment_feedback_factory,
):
    comment_1 = comment_factory(content_object=idea, is_moderator_marked=True)
    classification_1 = user_classification_factory(comment=comment_1, is_pending=False)

    comment_2 = comment_factory(content_object=idea, is_blocked=True)
    ai_classification_factory(
        comment=comment_2, is_pending=True, classification="OFFENSIVE"
    )
    ai_classification_factory(
        comment=comment_2, is_pending=True, classification="FACTCLAIMING"
    )
    classification_2 = ai_classification_factory(
        comment=comment_2, is_pending=False, classification="ENGAGING"
    )

    comment_3 = comment_factory(content_object=idea, is_removed=True)
    user_classification_factory(comment=comment_3, is_pending=True)
    classification_3 = ai_classification_factory(comment=comment_3, is_pending=True)
    feedback = moderator_comment_feedback_factory(comment=comment_3)

    with freeze_time(comment_2.created + timedelta(minutes=3)):
        comment_2.modified = timezone.now()
        comment_2.save()

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password="password")
    url = reverse("moderationcomments-list", kwargs={"project_pk": project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    comment_1_data = [
        comment for comment in response.data if comment["pk"] == comment_1.pk
    ][0]
    comment_2_data = [
        comment for comment in response.data if comment["pk"] == comment_2.pk
    ][0]
    comment_3_data = [
        comment for comment in response.data if comment["pk"] == comment_3.pk
    ][0]

    assert comment_1_data["category_counts"] == {
        "offensive": {"count": 1, "translated": "offensive"}
    }
    assert not comment_1_data["ai_classified"]
    assert comment_1_data["comment"] == comment_1.comment
    assert comment_1_data["comment_url"] == comment_1.get_absolute_url()
    assert not comment_1_data["has_pending_and_archived_notifications"]
    assert not comment_1_data["has_pending_notifications"]
    assert not comment_1_data["is_blocked"]
    assert comment_1_data["is_moderator_marked"]
    assert not comment_1_data["is_modified"]
    assert comment_1_data["last_edit"] == dates.get_date_display(comment_1.created)
    assert comment_1_data["moderator_feedback"] is None
    assert comment_1_data["num_active_notifications"] == 1
    assert comment_1_data["pk"] == comment_1.pk
    assert comment_1_data["feedback_api_url"] == reverse(
        "moderatorfeedback-list", kwargs={"comment_pk": comment_1.pk}
    )
    assert comment_1_data["time_of_last_notification"] == dates.get_date_display(
        classification_1.created
    )
    assert comment_1_data["user_image"] == comment_1.creator.avatar_fallback
    assert comment_1_data["user_name"] == comment_1.creator.username
    assert comment_1_data["user_profile_url"] == comment_1.creator.get_absolute_url()

    assert comment_2_data["category_counts"] == {
        "offensive": {"count": 1, "translated": "offensive"},
        "factclaiming": {"count": 1, "translated": "fact claiming"},
    }
    assert comment_2_data["comment"] == comment_2.comment
    assert comment_2_data["comment_url"] == comment_2.get_absolute_url()
    assert comment_2_data["has_pending_and_archived_notifications"]
    assert comment_2_data["has_pending_notifications"]
    assert comment_2_data["is_blocked"]
    assert not comment_2_data["is_moderator_marked"]
    assert comment_2_data["is_modified"]
    assert comment_2_data["last_edit"] == dates.get_date_display(comment_2.modified)
    assert comment_2_data["moderator_feedback"] is None
    assert comment_2_data["num_active_notifications"] == 2
    assert comment_2_data["pk"] == comment_2.pk
    assert comment_2_data["feedback_api_url"] == reverse(
        "moderatorfeedback-list", kwargs={"comment_pk": comment_2.pk}
    )
    assert comment_2_data["time_of_last_notification"] == dates.get_date_display(
        classification_2.created
    )
    assert comment_2_data["user_image"] == comment_2.creator.avatar_fallback
    assert comment_2_data["user_name"] == comment_2.creator.username
    assert comment_2_data["user_profile_url"] == comment_2.creator.get_absolute_url()

    assert comment_3_data["category_counts"] == {
        "offensive": {"count": 2, "translated": "offensive"}
    }
    assert comment_3_data["ai_classified"]
    assert comment_3_data["comment"] == comment_3.comment
    assert comment_3_data["comment_url"] == comment_3.get_absolute_url()
    assert not comment_3_data["has_pending_and_archived_notifications"]
    assert comment_3_data["has_pending_notifications"]
    assert not comment_3_data["is_blocked"]
    assert not comment_3_data["is_moderator_marked"]
    assert not comment_3_data["is_modified"]
    assert comment_3_data["last_edit"] == dates.get_date_display(comment_3.created)
    assert (
        comment_3_data["moderator_feedback"]["feedback_text"] == feedback.feedback_text
    )
    assert comment_3_data["num_active_notifications"] == 2
    assert comment_3_data["pk"] == comment_3.pk
    assert comment_3_data["feedback_api_url"] == reverse(
        "moderatorfeedback-list", kwargs={"comment_pk": comment_3.pk}
    )
    assert comment_3_data["time_of_last_notification"] == dates.get_date_display(
        classification_3.created
    )
    assert comment_3_data["user_image"] is None
    assert comment_3_data["user_name"] == "unknown user"
    assert comment_3_data["user_profile_url"] == ""
