from rest_framework import serializers

from authentication.models import KnownIdentity, FriendRequestIncoming, ToolshedUser
from toolshed.models import InventoryItem


class FriendSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = KnownIdentity
        fields = ['username', 'public_key']

    def get_username(self, obj):
        return obj.username + '@' + obj.domain


class FriendRequestSerializer(serializers.ModelSerializer):
    befriender = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequestIncoming
        fields = ['befriender', 'befriender_public_key', 'secret', 'id']

    def get_befriender(self, obj):
        return obj.befriender_username + '@' + obj.befriender_domain


class InventoryItemOwnerSerializer(serializers.ReadOnlyField):
    class Meta:
        model = ToolshedUser
        fields = '__all__'

    def to_representation(self, value):
        # TODO: this is a hack, fix it
        return value.username + '@' + value.domain


class InventoryItemSerializer(serializers.ModelSerializer):
    owner = InventoryItemOwnerSerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = '__all__'
