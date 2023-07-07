from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.signature_auth import SignatureAuthenticationLocal
from files.models import File
from files.serializers import FileSerializer
from toolshed.models import InventoryItem


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthenticationLocal])
def list_all_files(request, format=None):  # /files/
    files = File.objects.select_related().filter(connected_items__owner=request.user).distinct()
    return Response(FileSerializer(files, many=True).data)


def get_item_files(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id, owner=request.user)
        files = item.files.all()
        return Response(FileSerializer(files, many=True).data)
    except InventoryItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def post_item_file(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id, owner=request.user)
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            item.files.add(file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except InventoryItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthenticationLocal])
def item_files(request, item_id, format=None):  # /item_files/
    if request.method == 'GET':
        return get_item_files(request, item_id)
    elif request.method == 'POST':
        return post_item_file(request, item_id)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthenticationLocal])
def delete_item_file(request, item_id, file_id, format=None):  # /item_files/
    try:
        item = InventoryItem.objects.get(id=item_id, owner=request.user)
        file = item.files.get(id=file_id)
        item.files.remove(file_id)
        if file.connected_items.count() == 0:
            file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except InventoryItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


urlpatterns = [
    path('files/', list_all_files),
    path('item_files/<int:item_id>/', item_files),
    path('item_files/<int:item_id>/<int:file_id>/', delete_item_file),
]
