from rest_framework import serializers
from authentication.models import KnownIdentity


class FriendSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = KnownIdentity
        fields = ['username', 'public_key']

    def get_username(self, obj):
        return obj.username + '@' + obj.domain
