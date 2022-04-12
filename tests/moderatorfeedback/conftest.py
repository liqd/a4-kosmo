from pytest_factoryboy import register

from tests.ideas.factories import IdeaFactory

from .factories import ModeratorCommentStatementFactory

register(IdeaFactory)
register(ModeratorCommentStatementFactory)
