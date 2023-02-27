from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from adhocracy4.comments.models import Comment

from apps.classifications.models import AIClassification
from apps.classifications.models import UserClassification


def get_all_comments_project(project):
    return Comment.objects.filter(
        Q(project=project) | Q(parent_comment__project=project)
    )


def get_num_comments_project(project):
    return get_all_comments_project(project).count()


def get_num_user_classifications(project):
    comments_project = get_all_comments_project(project)
    return UserClassification.objects.filter(comment__in=comments_project).count()


def get_num_ai_classifications(project):
    comments_project = get_all_comments_project(project)
    return AIClassification.objects.filter(comment__in=comments_project).count()


def get_num_classifications(project):
    return get_num_user_classifications(project) + get_num_ai_classifications(project)


def get_num_latest_comments(project, until={"days": 7}):
    all_comments_project = get_all_comments_project(project)
    return all_comments_project.filter(
        created__gte=timezone.now() - timedelta(**until)
    ).count()
