from pytest_factoryboy import register

from tests.classifications import factories as classification_factories
from tests.ideas import factories as idea_factories

from . import factories as invites

register(invites.ModeratorInviteFactory)
register(invites.ParticipantInviteFactory)

register(classification_factories.AIClassificationFactory)
register(classification_factories.UserClassificationFactory)
register(idea_factories.IdeaFactory)
