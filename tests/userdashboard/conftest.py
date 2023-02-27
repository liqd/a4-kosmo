from pytest_factoryboy import register

from tests.classifications import factories
from tests.ideas.factories import IdeaFactory
from tests.moderatorfeedback.factories import ModeratorCommentFeedbackFactory

register(IdeaFactory)
register(factories.UserClassificationFactory)
register(factories.AIClassificationFactory)
register(ModeratorCommentFeedbackFactory)
