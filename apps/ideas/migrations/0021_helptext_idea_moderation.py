# Generated by Django 2.2.4 on 2019-09-09 13:16

import apps.moderatorfeedback.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_ideas', '0020_update_content_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='moderator_feedback',
            field=apps.moderatorfeedback.fields.ModeratorFeedbackField(blank=True, choices=[('CONSIDERATION', 'Under consideration'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted')], default=None, help_text='The editing status appears below the title of the idea in red, yellow or green. The idea provider receives a notification.', max_length=254, null=True, verbose_name='Processing status'),
        ),
    ]
