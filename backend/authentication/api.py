from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import ToolshedUser

router = routers.SimpleRouter()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ToolshedUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']


class UserViewSet(viewsets.ModelViewSet):
    queryset = ToolshedUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
def registerUser(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def userKeys(request):
    user = request.user
    return Response({'key': user.private_key})


router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', registerUser),
    path('keys/', userKeys),
]
