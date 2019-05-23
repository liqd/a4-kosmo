import pytest

from liqd_product.apps.polls import phases
from tests.helpers import assert_template_response
from tests.helpers import freeze_phase
from tests.helpers import setup_phase


@pytest.mark.django_db
def test_detail_view(client, phase_factory, poll_factory, question_factory,
                     choice_factory, partner):
    phase, module, project, item = setup_phase(
        phase_factory, poll_factory, phases.VotingPhase)
    question = question_factory(poll=item)
    choice_factory(question=question)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'a4_candy_polls/poll_detail.html')
