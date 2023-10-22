from rest_framework import serializers

from authentication.serializers import OwnerSerializer
from hostadmin.models import Domain
from toolshed.models import Category, Property, Tag


class DomainSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Domain
        fields = ['name', 'owner', 'open_registration']

    def create(self, validated_data):
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ['name', 'description', 'parent', 'origin']
        read_only_fields = ['origin']


class PropertySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), required=False)

    class Meta:
        model = Property
        fields = ['name', 'description', 'category', 'unit_symbol', 'unit_name', 'unit_name_plural', 'base2_prefix',
                  'dimensions', 'origin']
        read_only_fields = ['origin']


class TagSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), required=False)

    class Meta:
        model = Tag
        fields = ['name', 'description', 'category', 'origin']
        read_only_fields = ['origin']
