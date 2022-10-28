from django.contrib import admin

import block_schema
from RequestHeaders.models import *
from block_schema.models import BlockSchema


class BlockSchemaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BlockSchema._meta.fields]

    search_fields = [field.name for field in BlockSchema._meta.fields]

    class Meta:
        model = BlockSchema


admin.site.register(BlockSchema, BlockSchemaAdmin)
