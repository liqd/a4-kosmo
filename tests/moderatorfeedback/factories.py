import factory

from adhocracy4.test import factories as a4_factories
from apps.moderatorfeedback.models import ModeratorCommentStatement
from tests.factories import CommentFactory


class ModeratorCommentStatementFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ModeratorCommentStatement

    statement = factory.Faker('text')
    comment = factory.SubFactory(CommentFactory)
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
