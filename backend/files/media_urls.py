from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from files.models import File


@api_view(['GET'])
def media_urls(request, id, format=None):
    try:
        file = File.objects.get(file=id)
        return Response(status=status.HTTP_200_OK,
                        headers={'X-Accel-Redirect': f'/redirect_media/{id}'})  # TODO Expires and Cache-Control

    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


urlpatterns = [
    path('<path:id>', media_urls),
]
