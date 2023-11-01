from django.contrib import admin

from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'hash', 'mime_type', 'created_at', 'updated_at')
    list_filter = ('id', 'hash', 'mime_type', 'created_at', 'updated_at')


admin.site.register(File, FileAdmin)