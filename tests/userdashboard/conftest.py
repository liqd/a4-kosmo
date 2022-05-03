from pytest_factoryboy import register

from tests.classifications import factories
from tests.ideas.factories import IdeaFactory

register(IdeaFactory)
register(factories.UserClassificationFactory)
register(factories.AIClassificationFactory)
