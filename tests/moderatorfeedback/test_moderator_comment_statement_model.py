import pytest


@pytest.mark.django_db
def test_str(idea, comment_factory, moderator_comment_statement_factory):

    comment = comment_factory(pk=1, content_object=idea)
    statement = moderator_comment_statement_factory(
        comment=comment,
        statement='This is a statement.'
    )
    assert str(statement) == '1 - This is a statement.'


@pytest.mark.django_db
def test_project(idea, comment_factory, moderator_comment_statement_factory):

    comment = comment_factory(content_object=idea)
    statement = moderator_comment_statement_factory(
        comment=comment,
    )
    assert statement.project == comment.project
