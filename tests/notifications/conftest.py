from pytest_factoryboy import register

from tests.budgeting.factories import ProposalFactory
from tests.classifications.factories import AIClassificationFactory
from tests.ideas.factories import IdeaFactory
from tests.moderatorfeedback.factories import ModeratorCommentFeedbackFactory
from tests.offlineevents.factories import OfflineEventFactory

register(ProposalFactory)
register(AIClassificationFactory)
register(IdeaFactory)
register(ModeratorCommentFeedbackFactory)
register(OfflineEventFactory)
