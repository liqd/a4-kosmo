from pytest_factoryboy import register

from tests.ideas import factories as idea_factories
from tests.moderatorfeedback.factories import ModeratorCommentFeedbackFactory

from . import factories

register(idea_factories.IdeaFactory)
register(factories.UserClassificationFactory)
register(factories.AIClassificationFactory)
register(ModeratorCommentFeedbackFactory)
