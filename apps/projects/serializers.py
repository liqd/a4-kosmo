from functools import lru_cache

from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.categories.models import Category
from adhocracy4.labels.models import Label
from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project

from . import helpers


class AppProjectSerializer(serializers.ModelSerializer):

    information = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    # todo: remove many=True once AppProjects are restricted to single module
    published_modules = serializers.PrimaryKeyRelatedField(read_only=True,
                                                           many=True)
    organisation = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()
    single_agenda_setting_module = serializers.SerializerMethodField()
    single_poll_module = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('pk', 'name', 'description', 'information', 'result',
                  'organisation', 'published_modules', 'access', 'image',
                  'single_agenda_setting_module', 'single_poll_module')

    def get_information(self, project):
        return strip_tags(project.information)

    def get_result(self, project):
        return strip_tags(project.result)

    def get_organisation(self, project):
        return project.organisation.name

    def get_access(self, project):
        return project.access.name

    # todo: module logic has to be replaced once we introduced module types
    # currently only works because agenda setting is only module using phase
    # of type 'a4_candy_ideas:rating'
    def get_single_agenda_setting_module(self, project):
        if (project.published_modules.count() == 1 and
                any([True for phase in project.modules.first().phases
                    if phase.type == 'a4_candy_ideas:rating'])):
            return project.published_modules.first().pk
        return False

    def get_single_poll_module(self, project):
        if (project.published_modules.count() == 1 and
                project.published_modules.first().phases.count() == 1 and
                project.published_modules.first().phases.first().type
                == 'a4polls:voting'):
            return project.published_modules.first().pk
        return False


class AppPhaseSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Phase
        fields = ('name', 'description', 'type', 'start_date',
                  'end_date', 'is_active')

    def get_is_active(self, instance):
        if instance.start_date and instance.end_date:
            return (instance.start_date <= timezone.now()
                    and instance.end_date >= timezone.now())
        return False


class AppModuleSerializer(serializers.ModelSerializer):
    phases = AppPhaseSerializer(many=True, read_only=True)
    labels = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    has_idea_adding_permission = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ('pk', 'phases', 'labels', 'categories',
                  'has_idea_adding_permission')

    def get_labels(self, instance):
        labels = Label.objects.filter(module=instance)
        if labels:
            return [{'id': label.pk, 'name': label.name} for label in labels]
        return False

    def get_categories(self, instance):
        categories = Category.objects.filter(module=instance)
        if categories:
            return [{'id': category.pk, 'name': category.name}
                    for category in categories]
        return False

    def get_has_idea_adding_permission(self, instance):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            return user.has_perm('a4_candy_ideas.add_idea', instance)
        return False


class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    tile_image = serializers.SerializerMethodField()
    tile_image_copyright = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    future_phase = serializers.SerializerMethodField()
    active_phase = serializers.SerializerMethodField()
    past_phase = serializers.SerializerMethodField()
    offensive = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'url', 'organisation', 'tile_image',
                  'tile_image_copyright',
                  'status', 'access',
                  'participation_active',
                  'participation_string',
                  'future_phase', 'active_phase',
                  'past_phase',
                  'offensive', 'comment_count']

    @lru_cache(maxsize=1)
    def _get_participation_status_project(self, instance):
        project_phases = instance.phases

        if project_phases.active_phases():
            return _('running'), True

        if project_phases.future_phases():
            try:
                return (_('starts on {}').format
                        (project_phases.future_phases().first().
                         start_date.strftime('%d.%m.%y')),
                        True)
            except AttributeError:
                return (_('starts in the future'),
                        True)
        else:
            return _('completed'), False

    def get_type(self, instance):
        return 'project'

    def get_title(self, instance):
        return instance.name

    def get_url(self, instance):
        return instance.get_absolute_url()

    def get_organisation(self, instance):
        return instance.organisation.name

    def get_tile_image(self, instance):
        image_url = ''
        if instance.tile_image:
            image = get_thumbnailer(instance.tile_image)['project_thumbnail']
            image_url = image.url
        elif instance.image:
            image = get_thumbnailer(instance.image)['project_thumbnail']
            image_url = image.url
        return image_url

    def get_tile_image_copyright(self, instance):
        if instance.tile_image:
            return instance.tile_image_copyright
        elif instance.image:
            return instance.image_copyright
        else:
            return None

    def get_status(self, instance):
        project_phases = instance.phases
        if project_phases.active_phases() or project_phases.future_phases():
            return 0
        return 1

    def get_participation_active(self, instance):
        participation_string, participation_active = \
            self._get_participation_status_project(instance)
        return participation_active

    def get_participation_string(self, instance):
        participation_string, participation_active = \
            self._get_participation_status_project(instance)
        return str(participation_string)

    def get_future_phase(self, instance):
        if (instance.future_modules and
                instance.future_modules.first().module_start):
            return str(
                instance.future_modules.first().module_start)
        return False

    def get_active_phase(self, instance):
        if instance.active_phase_ends_next:
            progress = instance.module_running_progress
            time_left = instance.module_running_time_left
            end_date = str(instance.running_module_ends_next.module_end)
            return [progress, time_left, end_date]
        return False

    def get_past_phase(self, instance):
        if (instance.past_modules and
                instance.past_modules.first().module_end):
            return str(
                instance.past_modules.first().module_end)
        return False

    def get_offensive(self, instance):
        return helpers.get_num_reported_comments(instance)

    def get_comment_count(self, instance):
        return helpers.get_num_comments_project(instance)
