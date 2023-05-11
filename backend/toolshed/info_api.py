from django.urls import path
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from hostadmin.models import Domain


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def listDomains(request, format=None):  # /admin/domainlist/
    domains = [domain.name for domain in Domain.objects.filter(open_registration=True)]
    return Response(domains)


urlpatterns = [
    path('domains/', listDomains, name='domainlist'),
]
