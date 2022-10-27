from django.contrib import admin

import file
from RequestHeaders.models import *
from file.models import File, FilePart, ExternalLink


class FileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in File._meta.fields]

    search_fields = [field.name for field in File._meta.fields]

    class Meta:
        model = File


class FilePartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FilePart._meta.fields]

    search_fields = [field.name for field in FilePart._meta.fields]

    class Meta:
        model = FilePart



class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ExternalLink._meta.fields]

    search_fields = [field.name for field in ExternalLink._meta.fields]

    class Meta:
        model = ExternalLink


admin.site.register(File, FileAdmin)
admin.site.register(FilePart, FilePartAdmin)
admin.site.register(ExternalLink, ExternalLinkAdmin)

