# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 13:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    replaces = [('meinberlin_projects', '0001_initial')]

    initial = True

    dependencies = [
        ('a4projects', '0010_image_copyrights'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeratorInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('token', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a4projects.Project')),
            ],
            options={
                'abstract': False,
                'db_table': 'meinberlin_projects_moderatorinvite',
            },
        ),
        migrations.CreateModel(
            name='ParticipantInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('token', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a4projects.Project')),
            ],
            options={
                'abstract': False,
                'db_table': 'meinberlin_projects_participantinvite',
            },
        ),
        migrations.AlterUniqueTogether(
            name='participantinvite',
            unique_together=set([('email', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='moderatorinvite',
            unique_together=set([('email', 'project')]),
        ),
    ]
