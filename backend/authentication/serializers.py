from rest_framework import serializers

from authentication.models import ToolshedUser


class OwnerSerializer(serializers.ReadOnlyField):
    class Meta:
        model = ToolshedUser
        fields = ['username', 'domain']

    def to_representation(self, value):
        return value.username + '@' + value.domain
