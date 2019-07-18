from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import ObjectList
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import TabbedInterface
from wagtail.core import blocks
from wagtail.core import fields
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from apps.cms import blocks as cms_blocks
from apps.contrib.translations import TranslatedField


class HomePage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Header Image",
        help_text="The Image that is shown on top of the page"
    )

    subtitle_de = models.CharField(
        max_length=500, blank=True, verbose_name="Subtitle")
    subtitle_en = models.CharField(
        max_length=500, blank=True, verbose_name="Subtitle")

    body_de = fields.RichTextField(blank=True)
    body_en = fields.RichTextField(blank=True)

    body_streamfield_de = fields.StreamField([
        ('image_cta_block', cms_blocks.ColumnsImageCTABlock()),
        ('background_cta_block', cms_blocks.ColBackgroundCTABlock()),
        ('columns_cta', cms_blocks.ColumnsCTABlock()),
        ('html', blocks.RawHTMLBlock()),
        ('paragraph', blocks.RichTextBlock())
    ], blank=True)

    body_streamfield_en = fields.StreamField([
        ('image_cta_block', cms_blocks.ColumnsImageCTABlock()),
        ('background_cta_block', cms_blocks.ColBackgroundCTABlock()),
        ('columns_cta', cms_blocks.ColumnsCTABlock()),
        ('html', blocks.RawHTMLBlock()),
        ('paragraph', blocks.RichTextBlock())
    ], blank=True)

    body_streamfield = TranslatedField(
        'body_streamfield_de',
        'body_streamfield_en'
    )

    body = TranslatedField(
        'body_de',
        'body_en',
    )

    subtitle = TranslatedField(
        'subtitle_de',
        'subtitle_en'
    )

    en_content_panels = [
        FieldPanel('subtitle_en'),
        FieldPanel('body_en'),
        StreamFieldPanel('body_streamfield_en')
    ]

    de_content_panels = [
        FieldPanel('subtitle_de'),
        FieldPanel('body_de'),
        StreamFieldPanel('body_streamfield_de')
    ]

    common_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        ImageChooserPanel('image'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(common_panels, heading='Common'),
        ObjectList(en_content_panels, heading='English'),
        ObjectList(de_content_panels, heading='German')
    ])

    subpage_types = ['a4_candy_cms_pages.EmptyPage']


class EmptyPage(Page):
    subpage_types = ['a4_candy_cms_pages.SimplePage']


class SimplePage(Page):
    body_de = fields.RichTextField()
    body_en = fields.RichTextField(blank=True)

    body = TranslatedField(
        'body_de',
        'body_en'
    )

    en_content_panels = [
        FieldPanel('body_en')
    ]

    de_content_panels = [
        FieldPanel('body_de')
    ]

    common_panels = [
        FieldPanel('title'),
        FieldPanel('slug')
    ]

    edit_handler = TabbedInterface([
        ObjectList(common_panels, heading='Common'),
        ObjectList(en_content_panels, heading='English'),
        ObjectList(de_content_panels, heading='German')
    ])

    subpage_types = ['a4_candy_cms_pages.SimplePage']
