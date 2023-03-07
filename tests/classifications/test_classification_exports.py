import pytest

from apps.classifications.exports import AIClassificationExport
from apps.classifications.exports import UserClassificationExport


@pytest.mark.django_db
def test_ai_classifications_export(
    idea,
    comment_factory,
    ai_classification_factory,
    moderator_comment_statement_factory,
):

    comment_1 = comment_factory(content_object=idea)
    comment_2 = comment_factory(content_object=idea)
    moderator_statement = moderator_comment_statement_factory(comment=comment_1)
    ai_classification_1 = ai_classification_factory(comment=comment_1)
    ai_classification_2 = ai_classification_factory(
        comment=comment_2, classification="ENGAGING"
    )
    ai_classification_3 = ai_classification_factory(comment=comment_1)

    ai_classification_export = AIClassificationExport()

    header = ai_classification_export.get_header()
    assert header == [
        "ID",
        "Created",
        "classification",
        "comment text",
        "is pending",
        "comment_id",
        "comment_comment",
        "comment_is_blocked",
        "comment_is_moderator_marked",
        "comment_created",
        "comment_modified",
        "comment_moderator_statement",
    ]

    queryset = ai_classification_export.get_queryset()
    assert queryset.count() == 3
    assert ai_classification_1 == queryset.first()
    assert ai_classification_2 == queryset.last()
    assert ai_classification_3 in queryset

    assert ai_classification_export.get_field_data(
        ai_classification_1, "comment_id"
    ) == str(comment_1.id)
    assert (
        ai_classification_export.get_field_data(ai_classification_2, "classification")
        == "ENGAGING"
    )
    assert ai_classification_export.get_field_data(
        ai_classification_1, "comment_moderator_statement"
    ) == str(moderator_statement)
    assert (
        ai_classification_export.get_field_data(
            ai_classification_2, "comment_moderator_statement"
        )
        == ""
    )


@pytest.mark.django_db
def test_user_classifications_export(
    idea,
    comment_factory,
    user_classification_factory,
    moderator_comment_statement_factory,
):

    comment_1 = comment_factory(content_object=idea)
    comment_2 = comment_factory(content_object=idea)
    moderator_statement = moderator_comment_statement_factory(comment=comment_1)
    user_classification_1 = user_classification_factory(comment=comment_1)
    user_classification_2 = user_classification_factory(
        comment=comment_2, user_message="this needs to be reported"
    )

    user_classification_export = UserClassificationExport()

    header = user_classification_export.get_header()
    assert header == [
        "ID",
        "Created",
        "classification",
        "comment text",
        "is pending",
        "comment_id",
        "comment_comment",
        "comment_is_blocked",
        "comment_is_moderator_marked",
        "comment_created",
        "comment_modified",
        "comment_moderator_statement",
        "user message",
    ]

    queryset = user_classification_export.get_queryset()
    assert queryset.count() == 2
    assert user_classification_1 == queryset.first()
    assert user_classification_2 == queryset.last()

    assert user_classification_export.get_field_data(
        user_classification_1, "comment_id"
    ) == str(comment_1.id)
    assert (
        user_classification_export.get_field_data(user_classification_1, "user_message")
        == "This is bad."
    )
    assert (
        user_classification_export.get_field_data(user_classification_2, "user_message")
        == "this needs to be reported"
    )
    assert user_classification_export.get_field_data(
        user_classification_1, "comment_moderator_statement"
    ) == str(moderator_statement)
    assert (
        user_classification_export.get_field_data(
            user_classification_2, "comment_moderator_statement"
        )
        == ""
    )
