from django.contrib import admin

from toolshed.models import InventoryItem, Property, Tag, ItemProperty, ItemTag, LendingPeriod, Profile


class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'availability_policy', 'owned_amount', 'owner',)
    search_fields = ('name', 'description', 'category', 'availability_policy', 'owned_amount', 'owner',)


admin.site.register(InventoryItem, InventoryItemAdmin)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Property, PropertyAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)


class ItemPropertyAdmin(admin.ModelAdmin):
    list_display = ('item', 'property', 'value')
    search_fields = ('item', 'property', 'value')


admin.site.register(ItemProperty, ItemPropertyAdmin)


class ItemTagAdmin(admin.ModelAdmin):
    list_display = ('item', 'tag')
    search_fields = ('item', 'tag')


admin.site.register(ItemTag, ItemTagAdmin)


class LendingPeriodAdmin(admin.ModelAdmin):
    list_display = ('item', 'start_date', 'end_date')
    search_fields = ('item', 'start_date', 'end_date')


admin.site.register(LendingPeriod, LendingPeriodAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location')
    search_fields = ('user', 'bio', 'location')


admin.site.register(Profile, ProfileAdmin)


