from rest_framework import serializers
from authentication.models import KnownIdentity
from toolshed.models import Category, Property


class FriendSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = KnownIdentity
        fields = ['username', 'public_key']

    def get_username(self, obj):
        return obj.username + '@' + obj.domain


class PropertySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')

    class Meta:
        model = Property
        fields = ['name', 'description', 'category', 'unit_symbol', 'unit_name', 'unit_name_plural', 'base2_prefix']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def to_representation(self, instance):
        return str(instance)
