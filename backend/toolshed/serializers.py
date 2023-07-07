from rest_framework import serializers

from authentication.models import KnownIdentity, ToolshedUser
from authentication.serializers import OwnerSerializer
from files.models import File
from files.serializers import FileSerializer
from toolshed.models import Category, Property, ItemProperty, InventoryItem, Tag


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

    def to_internal_value(self, data):
        return Category.objects.get(name=data.split("/")[-1])


class ItemPropertySerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)

    class Meta:
        model = ItemProperty
        fields = ['property', 'value']

    def to_representation(self, instance):
        return {'value': instance.value, 'name': instance.property.name}

    def to_internal_value(self, data):
        prop = Property.objects.get(name=data['name'])
        value = data['value']
        return {'property': prop, 'value': value}


class InventoryItemSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    tags = serializers.SlugRelatedField(many=True, required=False, queryset=Tag.objects.all(), slug_field='name')
    properties = ItemPropertySerializer(many=True, required=False, source='itemproperty_set')
    category = CategorySerializer(required=False, allow_null=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'owner', 'category', 'availability_policy', 'owned_quantity', 'owner',
                  'tags', 'properties']

    def to_internal_value(self, data):
        files = data.pop('files', [])
        ret = super().to_internal_value(data)
        ret['files'] = files
        return ret

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        props = validated_data.pop('itemproperty_set', [])
        files = validated_data.pop('files', [])
        item = InventoryItem.objects.create(**validated_data)
        for tag in tags:
            item.tags.add(tag, through_defaults={})
        for prop in props:
            ItemProperty.objects.create(inventory_item=item, property=prop['property'], value=prop['value'])
        for file in files:
            if type(file) == dict:
                file_serializer = FileSerializer(data=file)
                if file_serializer.is_valid():
                    file_serializer.save()
                    item.files.add(file_serializer.instance)
                else:
                    raise serializers.ValidationError(file_serializer.errors)
            elif type(file) == int:
                if File.objects.filter(id=file).exists():
                    item.files.add(File.objects.get(id=file))
                else:
                    raise serializers.ValidationError("File with id {} does not exist".format(file))
        item.save()
        return item

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        props = validated_data.pop('itemproperty_set', [])
        item = super().update(instance, validated_data)
        item.tags.clear()
        item.properties.clear()
        if 'category' not in validated_data:
            item.category = None
        for tag in tags:
            item.tags.add(tag)
        for prop in props:
            ItemProperty.objects.create(inventory_item=item, property=prop['property'], value=prop['value'])
        item.save()
        return item
