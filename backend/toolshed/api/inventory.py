from django.urls import path
from rest_framework import routers, viewsets
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import ToolshedUser
from authentication.signature_auth import SignatureAuthentication
from toolshed.models import InventoryItem
from toolshed.serializers import InventoryItemSerializer

router = routers.SimpleRouter()


def inventory_items(identity):
    try:
        user = identity.user.get()
        if user:
            for item in user.inventory_items.all():
                yield item
    except ToolshedUser.DoesNotExist:
        pass
    for friend in identity.friends.all():
        if friend_user := friend.user.get():
            for item in friend_user.inventory_items.all():
                yield item


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    authentication_classes = [SignatureAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user.user.get())

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.user.get())

    def perform_update(self, serializer):
        if serializer.instance.owner == self.request.user.user.get():
            serializer.save()

    def perform_destroy(self, instance):
        if instance.owner == self.request.user.user.get():
            instance.delete()


@api_view(['GET'])
@authentication_classes([SignatureAuthentication])
@permission_classes([IsAuthenticated])
def search_inventory_items(request):
    query = request.query_params.get('query')
    if query:
        return Response(InventoryItemSerializer(inventory_items(request.user), many=True).data)
    return Response({'error': 'No query provided.'}, status=400)


router.register(r'inventory_items', InventoryItemViewSet, basename='inventory_items')

urlpatterns = router.urls + [
    path('search/', search_inventory_items, name='search_inventory_items'),
]
