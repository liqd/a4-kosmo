# Generated by Django 2.2.4 on 2019-08-22 09:41

from django.db import migrations, models
import django.db.models.deletion


def set_custom_image_id(apps, schema_editor):
    CustomImage = apps.get_model('a4_candy_cms_images', 'CustomImage')
    HomePage = apps.get_model('a4_candy_cms_pages', 'HomePage')

    for page in HomePage.objects.all():
        if page.image:
            image = page.image
            page.custom_image_id = CustomImage.objects.get(id=image.id)
            page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_cms_images', '0002_copy_images'),
        ('a4_candy_cms_pages', '0019_auto_20190812_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='custom_image',
            field=models.ForeignKey(blank=True, help_text='The Image that is shown on top of the page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='a4_candy_cms_images.CustomImage', verbose_name='Header Image'),
        ),
        migrations.RunPython(set_custom_image_id),
    ]
