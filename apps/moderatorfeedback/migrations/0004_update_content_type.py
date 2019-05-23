# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-21 14:16
from __future__ import unicode_literals

from django.db import migrations

sql = """UPDATE django_content_type
         SET app_label = 'a4_candy_moderatorfeedback'
         WHERE app_label = 'liqd_product_moderatorfeedback';"""

reverse_sql = """UPDATE django_content_type
                 SET app_label = 'liqd_product_moderatorfeedback';
                 WHERE app_label = 'a4_candy_moderatorfeedback';"""


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_moderatorfeedback', '0003_rename_table_to_default'),
    ]

    operations = [
        migrations.RunSQL(sql, reverse_sql)
    ]
