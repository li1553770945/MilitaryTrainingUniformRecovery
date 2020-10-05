from django.contrib import admin
from .models import RecordModel


# Register your models here.

class RecordAdmin(admin.ModelAdmin):
    list_display_links = ['name', 'stu_id', 'manager']
    search_fields = ['name', 'stu_id']
    list_display = ['name', 'stu_id', 'manager']
    readonly_fields = ['time']


admin.site.register(RecordModel, RecordAdmin)
