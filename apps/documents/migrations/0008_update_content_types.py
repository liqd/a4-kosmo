# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-27 14:58
from __future__ import unicode_literals

from django.db import migrations

sql = """UPDATE django_content_type
         SET app_label = 'liqd_product_documents'
         WHERE app_label = 'meinberlin_documents';"""

reverse_sql = """UPDATE django_content_type
                 SET app_label = 'meinberlin_documents';
                 WHERE app_label = 'liqd_product_documents';"""


class Migration(migrations.Migration):

    replaces = [('liqd_product_documents', '0008_update_content_types')]

    dependencies = [
        ('a4_candy_documents', '0007_update_text_field'),
    ]

    operations = [
        migrations.RunSQL(sql, reverse_sql)
    ]
