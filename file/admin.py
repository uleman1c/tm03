from django.contrib import admin

import file
from RequestHeaders.models import *
from file.models import File, FilePart


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


admin.site.register(File, FileAdmin)
admin.site.register(FilePart, FilePartAdmin)
