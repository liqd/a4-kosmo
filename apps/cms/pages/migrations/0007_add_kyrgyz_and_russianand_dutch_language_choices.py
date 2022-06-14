# Generated by Django 2.2.19 on 2021-03-04 15:03

import apps.cms.blocks
from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_cms_pages', '0006_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplepage',
            name='body_streamfield_ky',
            field=wagtail.fields.StreamField([('html', wagtail.blocks.RawHTMLBlock()), ('richtext', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('faq', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('entries', wagtail.blocks.ListBlock(apps.cms.blocks.AccordeonBlock))])), ('image_cta', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))])), ('col_list_image_cta_block', wagtail.blocks.StructBlock([('columns_count', wagtail.blocks.ChoiceBlock(choices=[(1, 'One column'), (2, 'Two columns')])), ('columns', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))], label='List and Image')))])), ('columns_cta', wagtail.blocks.StructBlock([('columns_count', wagtail.blocks.ChoiceBlock(choices=[(1, 'One column'), (2, 'Two columns'), (3, 'Three columns')])), ('columns', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))], label='CTA Column')))])), ('downloads', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('documents', wagtail.blocks.ListBlock(apps.cms.blocks.DownloadBlock))])), ('quote', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('turquoise', 'turquoise'), ('blue', 'dark blue')])), ('image', wagtail.images.blocks.ImageChooserBlock()), ('quote', wagtail.blocks.TextBlock()), ('quote_author', wagtail.blocks.CharBlock(required=False)), ('link', wagtail.blocks.URLBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))]))], blank=True),
        ),
        migrations.AddField(
            model_name='simplepage',
            name='body_streamfield_nl',
            field=wagtail.fields.StreamField([('html', wagtail.blocks.RawHTMLBlock()), ('richtext', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('faq', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('entries', wagtail.blocks.ListBlock(apps.cms.blocks.AccordeonBlock))])), ('image_cta', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))])), ('col_list_image_cta_block', wagtail.blocks.StructBlock([('columns_count', wagtail.blocks.ChoiceBlock(choices=[(1, 'One column'), (2, 'Two columns')])), ('columns', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))], label='List and Image')))])), ('columns_cta', wagtail.blocks.StructBlock([('columns_count', wagtail.blocks.ChoiceBlock(choices=[(1, 'One column'), (2, 'Two columns'), (3, 'Three columns')])), ('columns', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))], label='CTA Column')))])), ('downloads', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('documents', wagtail.blocks.ListBlock(apps.cms.blocks.DownloadBlock))])), ('quote', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('turquoise', 'turquoise'), ('blue', 'dark blue')])), ('image', wagtail.images.blocks.ImageChooserBlock()), ('quote', wagtail.blocks.TextBlock()), ('quote_author', wagtail.blocks.CharBlock(required=False)), ('link', wagtail.blocks.URLBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))]))], blank=True),
        ),
        migrations.AddField(
            model_name='simplepage',
            name='body_streamfield_ru',
            field=wagtail.fields.StreamField([('html', wagtail.blocks.RawHTMLBlock()), ('richtext', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('faq', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('entries', wagtail.blocks.ListBlock(apps.cms.blocks.AccordeonBlock))])), ('image_cta', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))])), ('col_list_image_cta_block', wagtail.blocks.StructBlock([('columns_count', wagtail.blocks.ChoiceBlock(choices=[(1, 'One column'), (2, 'Two columns')])), ('columns', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))], label='List and Image')))])), ('columns_cta', wagtail.blocks.StructBlock([('columns_count', wagtail.blocks.ChoiceBlock(choices=[(1, 'One column'), (2, 'Two columns'), (3, 'Three columns')])), ('columns', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=False)), ('link', wagtail.blocks.CharBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))], label='CTA Column')))])), ('downloads', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('documents', wagtail.blocks.ListBlock(apps.cms.blocks.DownloadBlock))])), ('quote', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('turquoise', 'turquoise'), ('blue', 'dark blue')])), ('image', wagtail.images.blocks.ImageChooserBlock()), ('quote', wagtail.blocks.TextBlock()), ('quote_author', wagtail.blocks.CharBlock(required=False)), ('link', wagtail.blocks.URLBlock(required=False)), ('link_text', wagtail.blocks.CharBlock(label='Link Text', max_length=50, required=False))]))], blank=True),
        ),
    ]
