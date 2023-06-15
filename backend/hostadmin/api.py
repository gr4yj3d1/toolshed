from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from hostadmin.models import Domain

router = routers.SimpleRouter()


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


router.register(r'domains', DomainViewSet, basename='domains')

urlpatterns = [
    *router.urls,
]
