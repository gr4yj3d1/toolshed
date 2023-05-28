from rest_framework import routers, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from toolshed.auth import SignatureAuthentication
from toolshed.models import InventoryItem
from toolshed.serializers import InventoryItemSerializer

router = routers.SimpleRouter()


def inventory_items(identity):
    user = identity.user.get()
    if user:
        for item in user.inventory_items.all():
            yield item
    for friend in identity.friends.all():
        for item in friend.inventory_items.all():
            yield item


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    authentication_classes = [SignatureAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return inventory_items(user)
        else:
            return InventoryItem.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.user.get())


router.register(r'inventory_items', InventoryItemViewSet, basename='inventory_items')

urlpatterns = router.urls
