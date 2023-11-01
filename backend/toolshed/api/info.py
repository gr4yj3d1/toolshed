from django.urls import path
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hostadmin.models import Domain
from authentication.signature_auth import SignatureAuthentication
from toolshed.models import Tag, Property, Category
from toolshed.serializers import CategorySerializer, PropertySerializer
from backend.settings import TOOLSHED_VERSION


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_version(request, format=None):  # /version/
    return Response({'version': TOOLSHED_VERSION})


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def list_domains(request, format=None):  # /domains/
    domains = [domain.name for domain in Domain.objects.filter(open_registration=True)]
    return Response(domains)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthentication])
def list_tags(format=None):  # /tags/
    tags = [tag.name for tag in Tag.objects.all()]
    return Response(tags)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthentication])
def list_properties(request, format=None):  # /properties/
    return Response(PropertySerializer(Property.objects.all(), many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthentication])
def list_categories(request, format=None):  # /categories/
    return Response(CategorySerializer(Category.objects.all(), many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthentication])
def list_availability_policies(request, format=None):  # /availability_policies/
    policies = ['private', 'friends', 'internal', 'public']
    return Response(policies)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthentication])
def combined_info(request, format=None):  # /info/
    tags = [tag.name for tag in Tag.objects.all()]
    properties = PropertySerializer(Property.objects.all(), many=True).data
    categories = [str(category) for category in Category.objects.all()]
    policies = ['private', 'friends', 'internal', 'public']
    domains = [domain.name for domain in Domain.objects.filter(open_registration=True)]
    return Response({'tags': tags, 'properties': properties, 'availability_policies': policies, 'categories': categories, 'domains': domains})


urlpatterns = [
    path('version/', get_version, name='version'),
    path('availability_policies/', list_availability_policies, name='availability_policies'),
    path('properties/', list_properties, name='propertylist'),
    path('categories/', list_categories, name='categorylist'),
    path('domains/', list_domains, name='domainlist'),
    path('tags/', list_tags, name='taglist'),
    path('info/', combined_info, name='info'),
]
