from django.contrib import admin

import file
from RequestHeaders.models import *
from file.models import File, FileOwner, FilePart, ExternalLink, FileVersion, UploadlLink


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

class UploadlLinkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UploadlLink._meta.fields]

    search_fields = [field.name for field in UploadlLink._meta.fields]

    class Meta:
        model = UploadlLink


class FileOwnerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FileOwner._meta.fields]

    search_fields = [field.name for field in FileOwner._meta.fields]

    class Meta:
        model = FileOwner


class FileVersionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FileVersion._meta.fields]

    search_fields = [field.name for field in FileVersion._meta.fields]

    class Meta:
        model = FileVersion


admin.site.register(File, FileAdmin)
admin.site.register(FilePart, FilePartAdmin)
admin.site.register(ExternalLink, ExternalLinkAdmin)
admin.site.register(UploadlLink, UploadlLinkAdmin)
admin.site.register(FileOwner, FileOwnerAdmin)
admin.site.register(FileVersion, FileVersionAdmin)

