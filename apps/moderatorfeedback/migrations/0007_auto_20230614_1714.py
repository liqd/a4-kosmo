# Generated by Django 3.2.19 on 2023-06-14 15:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("a4comments", "0013_set_project"),
        ("a4_candy_moderatorfeedback", "0006_auto_20230614_1712"),
    ]

    operations = [
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
        migrations.AlterField(
            model_name="moderatorcommentfeedback",
            name="created",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="Created",
            ),
        ),
        migrations.AlterField(
            model_name="moderatorcommentfeedback",
            name="modified",
            field=models.DateTimeField(
                blank=True, editable=False, null=True, verbose_name="Modified"
            ),
        ),
    ]
