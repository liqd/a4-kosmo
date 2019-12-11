from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class DebatePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'debate'
    view = views.SubjectListView

    name = _('Debate phase')
    description = _('Debate topics.')
    module_name = _('topic debate')

    features = {
        'comment': (models.Subject,)
    }


phases.content.register(DebatePhase())
