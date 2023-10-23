from django.contrib import admin

from toolshed.models import InventoryItem, Property, Tag, ItemProperty, ItemTag


class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'availability_policy', 'owned_quantity', 'owner')
    search_fields = ('name', 'description', 'category', 'availability_policy', 'owned_quantity', 'owner')


admin.site.register(InventoryItem, InventoryItemAdmin)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Property, PropertyAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
