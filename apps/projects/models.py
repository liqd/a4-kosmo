import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from adhocracy4.models import base
from adhocracy4.projects.models import Project

from . import emails


class Invite(base.TimeStampedModel):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    site = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def accept(self, user):
        self.delete()

    def reject(self):
        self.delete()


class ParticipantInviteManager(models.Manager):
    def invite(self, creator, project, email, site):
        invite = super().create(
            project=project, creator=creator, email=email, site=site
        )
        emails.InviteParticipantEmail.send(invite)
        return invite


class ParticipantInvite(Invite):

    objects = ParticipantInviteManager()

    def __str__(self):
        return "Participation invite to {s.project} for {s.email}".format(s=self)

    def get_absolute_url(self):
        url_kwargs = {
            "organisation_slug": self.project.organisation.slug,
            "invite_token": self.token,
        }
        return reverse("project-participant-invite-detail", kwargs=url_kwargs)

    def accept(self, user):
        self.project.participants.add(user)
        super().accept(user)

    class Meta:
        unique_together = ("email", "project")


class ModeratorInviteManager(models.Manager):
    def invite(self, creator, project, email, site):
        invite = super().create(
            project=project, creator=creator, email=email, site=site
        )
        emails.InviteModeratorEmail.send(invite)
        return invite


class ModeratorInvite(Invite):

    objects = ModeratorInviteManager()

    def __str__(self):
        return "Moderation invite to {s.project} for {s.email}".format(s=self)

    def get_absolute_url(self):
        url_kwargs = {
            "organisation_slug": self.project.organisation.slug,
            "invite_token": self.token,
        }
        return reverse("project-moderator-invite-detail", kwargs=url_kwargs)

    def accept(self, user):
        self.project.moderators.add(user)
        super().accept(user)

    class Meta:
        unique_together = ("email", "project")
