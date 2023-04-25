from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from toolshed.auth import SignatureAuthentication
from toolshed.models import InventoryItem

router = routers.SimpleRouter()


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    authentication_classes = [SignatureAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return InventoryItem.objects.filter(owner=user)
        else:
            return InventoryItem.objects.none()


router.register(r'inventory_items', InventoryItemViewSet, basename='inventory_items')

urlpatterns = router.urls
