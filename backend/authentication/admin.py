from django.contrib import admin

from authentication.models import ToolshedUser, KnownIdentity, FriendRequestOutgoing, FriendRequestIncoming


class ToolshedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'domain')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'domain')


class KnownIdentityAdmin(admin.ModelAdmin):
    list_display = ('username', 'domain', 'public_key')
    search_fields = ('username', 'domain', 'public_key')


class FriendRequestOutgoingAdmin(admin.ModelAdmin):
    list_display = ('secret', 'befriender_user', 'befriendee_username', 'befriendee_domain')
    search_fields = ('secret', 'befriender_user', 'befriendee_username', 'befriendee_domain')


class FriendRequestIncomingAdmin(admin.ModelAdmin):
    list_display = ('secret', 'befriender_username', 'befriender_domain', 'befriendee_user', 'befriender_public_key')
    search_fields = ('secret', 'befriender_username', 'befriender_domain', 'befriendee_user', 'befriender_public_key')


admin.site.register(ToolshedUser, ToolshedUserAdmin)
admin.site.register(KnownIdentity, KnownIdentityAdmin)
admin.site.register(FriendRequestOutgoing, FriendRequestOutgoingAdmin)
admin.site.register(FriendRequestIncoming, FriendRequestIncomingAdmin)
