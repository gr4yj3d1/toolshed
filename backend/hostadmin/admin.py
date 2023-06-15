from django.contrib import admin

from .models import Domain


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'open_registration')
    list_filter = ('name', 'owner', 'open_registration')


admin.site.register(Domain, DomainAdmin)
