from rest_framework import routers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from authentication.signature_auth import SignatureAuthenticationLocal
from hostadmin.models import Domain
from hostadmin.serializers import DomainSerializer, CategorySerializer, PropertySerializer, TagSerializer
from toolshed.models import Category, Property, Tag

router = routers.SimpleRouter()


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    authentication_classes = [TokenAuthentication, SignatureAuthenticationLocal]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication, SignatureAuthenticationLocal]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(origin='api')


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    authentication_classes = [TokenAuthentication, SignatureAuthenticationLocal]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(origin='api')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication, SignatureAuthenticationLocal]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(origin='api')


router.register(r'domains', DomainViewSet, basename='domains')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    *router.urls,
]
