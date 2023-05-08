from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from authentication.models import ToolshedUser
from toolshed.auth import SignatureAuthentication
from toolshed.models import InventoryItem

router = routers.SimpleRouter()


class InventoryItemOwnerSerializer(serializers.ReadOnlyField):
    class Meta:
        model = ToolshedUser
        fields = '__all__'

    def to_representation(self, value):
        # TODO: this is a hack, fix it
        return value.username + '@domain.todo'


class InventoryItemSerializer(serializers.ModelSerializer):
    owner = InventoryItemOwnerSerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = '__all__'


def inventory_items(user):
    for friend in user.friends.all():
        for item in friend.inventory_items.all():
            yield item


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    authentication_classes = [SignatureAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return inventory_items(user)
        else:
            return InventoryItem.objects.none()


router.register(r'inventory_items', InventoryItemViewSet, basename='inventory_items')

urlpatterns = router.urls
