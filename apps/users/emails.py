from email.mime.image import MIMEImage

import sib_api_v3_sdk
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from sentry_sdk import capture_exception
from sib_api_v3_sdk.rest import ApiException
from wagtail.models import Site

from adhocracy4.emails import Email
from adhocracy4.emails.mixins import SyncEmailMixin
from apps.cms.settings.models import ImportantPages

from .models import User

ACCOUNT_LINK_TEXT = _(
    "If you no longer want to receive any notifications, "
    "change the settings for your {}account{}."
)
PROJECT_LINK_TEXT = _(
    "If you no longer want to receive notifications about "
    "this project, unsubscribe from the {}project{}."
)

# Translators: KOSMO
NETIQUETTE_LINK_TEXT = _("It does not correspond to the {}netiquette{}.")



class EmailAplus(Email):
    def get_languages(self, receiver):
        languages = super().get_languages(receiver)
        organisation = self.get_organisation()
        if User.objects.filter(email=receiver).exists():
            languages.insert(0, User.objects.get(email=receiver).language)
        elif organisation is not None:
            languages.insert(0, organisation.language)
        elif hasattr(settings, "DEFAULT_USER_LANGUAGE_CODE"):
            languages.insert(0, settings.DEFAULT_USER_LANGUAGE_CODE)

        return languages

    def get_receiver_language(self, receiver):
        return self.get_languages(receiver)[0]

    def get_context(self):
        context = super().get_context()
        context["organisation"] = self.get_organisation()
        return context

    def get_attachments(self):
        attachments = super().get_attachments()

        organisation = self.get_organisation()
        if organisation and organisation.logo:
            f = open(organisation.logo.path, "rb")
            logo = MIMEImage(f.read())
            logo.add_header("Content-ID", "<{}>".format("organisation_logo"))
            attachments += [logo]
            # need to remove standard email logo bc some email clients
            # display all attachments, even if not used
            attachments = [a for a in attachments if a["Content-Id"] != "<logo>"]

        return attachments

    def render(self, template_name, context):
        template = get_template(template_name + ".en.email")
        language = self.get_receiver_language(context["receiver"])
        with translation.override(language):
            context["account_link"] = self.get_html_link(
                ACCOUNT_LINK_TEXT, reverse("account")
            )
            if "action" in context:
                project = context["action"].project
                if project:
                    context["project_link"] = self.get_html_link(
                        PROJECT_LINK_TEXT, project.get_absolute_url()
                    )
            if "netiquette_url" in context and context["netiquette_url"]:
                context["netiquette_link"] = \
                    self.get_html_link(NETIQUETTE_LINK_TEXT,
                                       context["netiquette_url"])

            parts = []
            for part_type in ("subject", "txt", "html"):
                context["part_type"] = part_type
                parts.append(template.render(context))
                context.pop("part_type")
        return tuple(parts)

    def get_html_link(self, link_text, url):

        link = link_text.format(
            '<a href="' + self.get_host() + url + '" target="_blank">', "</a>"
        )
        return link


class WelcomeEmail(SyncEmailMixin, EmailAplus):

    def get_receivers(self):
        receiver = self.object
        return [receiver]

    def get_overview_link(self):
        url = reverse('userdashboard-overview')
        link = self.get_host() + url
        return link

    def get_getting_started_link(self):
        site = Site.objects.filter(
            is_default_site=True
        ).first()
        important_pages = ImportantPages.for_site(site)
        if getattr(important_pages, 'platform_information') and \
                getattr(important_pages, 'platform_information').live:
            url = getattr(important_pages, 'platform_information').url
            return self.get_host() + url
        return self.get_overview_link()

    def get_template_id(self, receiver):
        language = self.get_receiver_language(receiver)
        try:
            template_id = settings.SENDINBLUE_TEMPLATES[language]
        except KeyError:
            template_id = settings.SENDINBLUE_TEMPLATES[
                settings.DEFAULT_USER_LANGUAGE_CODE
            ]
        return template_id

    def dispatch(self, object, *args, **kwargs):
        self.object = object
        receiver = self.get_receivers()[0]

        if (hasattr(settings, 'SENDINBLUE_API_KEY') and
                hasattr(settings, 'SENDINBLUE_TEMPLATES')):
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY

            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuration)
            )

            to = [{"email": receiver.email, "NACHNAME": receiver.username}]
            template_id = self.get_template_id(receiver)
            params = {
                "username": receiver.username,
                "user_overview": self.get_overview_link(),
                "getting_started": self.get_getting_started_link(),
            }
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=to,
                template_id=template_id,
                params=params
            )
            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                if settings.DEBUG:
                    print(api_response)
                return HttpResponse(status=204)
            except ApiException as e:
                if settings.DEBUG:
                    print("Exception when calling "
                          "TransactionalEmailsApi->send_smtp_email: %s\n" % e)
                else:
                    capture_exception(e)
        else:
            raise ImproperlyConfigured(
                'Please make sure SENDINBLUE_API_KEY and SENDINBLUE_TEMPLATES '
                'are set in settings.')
