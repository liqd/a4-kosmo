# Generated by Django 3.2.19 on 2023-06-19 09:17

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('a4comments', '0013_set_project'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('a4_candy_moderatorfeedback', '0006_verbose_name_created_modified'),
    ]

    operations = [
        migrations.RenameModel(
            "ModeratorCommentStatement",
            "ModeratorCommentFeedback",
        ),
        migrations.RenameField(
            model_name="moderatorcommentfeedback",
            old_name="statement",
            new_name="feedback_text",
        ),
        migrations.AlterField(
            model_name="moderatorcommentfeedback",
            name="comment",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="moderator_feedback",
                to="a4comments.comment",
            ),
        ),
    ]
