# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 17:20
from __future__ import unicode_literals

import adhocracy4.images.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liqd_product_partners', '0003_rename_about_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='image',
            field=adhocracy4.images.fields.ConfiguredImageField('heroimage', blank=True, help_prefix='The image will be shown as a decorative background image.', upload_to='partners/backgrounds', verbose_name='Header image'),
        ),
    ]
