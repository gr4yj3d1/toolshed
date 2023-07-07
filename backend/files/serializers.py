from django.core.files.base import ContentFile
from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.Serializer):
    data = serializers.CharField()
    mime_type = serializers.CharField()
    class Meta:
        model = File
        fields = ['data', 'mime_type']
        read_only_fields = ['id', 'size', 'name']

    def to_representation(self, instance):
        return {'id': instance.id, 'name': instance.file.url, 'size': instance.file.size,
                'mime_type': instance.mime_type}

    def create(self, validated_data):
        return File.objects.get_or_create(**validated_data)[0]
