from django.contrib import admin
from django.urls import re_path

from . import exports
from . import models


class AIClassificationAdmin(admin.ModelAdmin):

    change_list_template = (
        'admin/a4_candy_classifications/object_tools_change_list.html'
    )

    def get_urls(self):
        urls = super().get_urls()
        export_urls = [
            re_path('export/',
                    exports.AIClassificationExport.as_view(),
                    name='aiclassification-export'),
        ]
        return export_urls + urls


class UserClassificationAdmin(admin.ModelAdmin):

    change_list_template = (
        'admin/a4_candy_classifications/object_tools_change_list.html'
    )

    def get_urls(self):
        urls = super().get_urls()
        export_urls = [
            re_path('export/',
                    exports.UserClassificationExport.as_view(),
                    name='userclassification-export'),
        ]
        return export_urls + urls


admin.site.register(models.UserClassification, UserClassificationAdmin)
admin.site.register(models.AIClassification, AIClassificationAdmin)
