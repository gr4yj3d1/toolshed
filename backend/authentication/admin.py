from django.contrib import admin

from authentication.models import ToolshedUser, KnownIdentity, FriendRequestOutgoing, FriendRequestIncoming


class ToolshedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'domain')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'domain')


class KnownIdentityAdmin(admin.ModelAdmin):
    list_display = ('username', 'domain', 'public_key')
    search_fields = ('username', 'domain', 'public_key')


class FriendRequestOutgoingAdmin(admin.ModelAdmin):
    list_display = ('nonce', 'from_user', 'to_username', 'to_domain', 'created_at')
    search_fields = ('nonce', 'from_user', 'to_username', 'to_domain', 'created_at')


class FriendRequestIncomingAdmin(admin.ModelAdmin):
    list_display = ('nonce', 'from_username')
    search_fields = ('nonce', 'from_username')


admin.site.register(ToolshedUser, ToolshedUserAdmin)
admin.site.register(KnownIdentity, KnownIdentityAdmin)
admin.site.register(FriendRequestOutgoing, FriendRequestOutgoingAdmin)
admin.site.register(FriendRequestIncoming, FriendRequestIncomingAdmin)
