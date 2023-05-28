from django.urls import path
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from hostadmin.models import Domain
from toolshed.models import Tag, Property


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def listDomains(request, format=None):  # /domains/
    domains = [domain.name for domain in Domain.objects.filter(open_registration=True)]
    return Response(domains)


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def listTags(request, format=None):  # /tags/
    tags = [tag.name for tag in Tag.objects.all()]
    return Response(tags)


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def listProperties(request, format=None):  # /properties/
    properties = [property.name for property in Property.objects.all()]
    return Response(properties)


urlpatterns = [
    path('properties/', listProperties, name='propertylist'),
    path('domains/', listDomains, name='domainlist'),
    path('tags/', listTags, name='taglist'),
]
