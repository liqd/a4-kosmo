# Generated by Django 3.2.19 on 2023-06-14 15:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("a4comments", "0013_set_project"),
        ("a4_candy_moderatorfeedback", "0005_merge_20230307_1614"),
    ]

    operations = [
        migrations.RenameModel(
            "ModeratorCommentStatement",
            "ModeratorCommentFeedback",
        )
    ]
