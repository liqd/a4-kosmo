# Generated by Django 2.2.20 on 2021-04-27 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_classifications', '0002_userclassification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aiclassification',
            name='classification',
            field=models.CharField(choices=[('OFFENSIVE', 'offensive'), ('OTHER', 'other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userclassification',
            name='classification',
            field=models.CharField(choices=[('OFFENSIVE', 'offensive'), ('OTHER', 'other')], max_length=50),
        ),
    ]