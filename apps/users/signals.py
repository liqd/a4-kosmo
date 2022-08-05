from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from adhocracy4.follows.models import Follow
from adhocracy4.projects.models import Project
from apps.cms.settings.models import OrganisationSettings


@receiver(user_signed_up)
def auto_follow_sample_project(request, user, **kwargs):
    organisation_settings = OrganisationSettings.for_request(request)
    if organisation_settings.sample_project_slug:
        try:
            sample_project = Project.objects.get(
                slug=organisation_settings.sample_project_slug)
            Follow.objects.create(creator=user, project=sample_project)
        except Project.DoesNotExist:
            pass
