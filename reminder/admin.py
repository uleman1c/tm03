from django.contrib import admin

from reminder.models import Reminder

# Register your models here.

class ReminderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reminder._meta.fields]

    search_fields = [field.name for field in Reminder._meta.fields]

    class Meta:
        model = Reminder


admin.site.register(Reminder, ReminderAdmin)

