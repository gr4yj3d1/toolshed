from django.http import HttpResponse
from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.signature_auth import SignatureAuthentication
from files.models import File


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthentication])
def media_urls(request, hash_path):
    try:
        file = File.objects.filter(connected_items__owner__in=request.user.friends_or_self()).distinct().get(
            file=hash_path)

        return HttpResponse(status=status.HTTP_200_OK,
                            content_type=file.mime_type,
                            headers={
                                'X-Accel-Redirect': f'/redirect_media/{hash_path}',
                                'Access-Control-Allow-Origin': '*',
                            })  # TODO Expires and Cache-Control

    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


urlpatterns = [
    path('<path:hash_path>', media_urls),
]
