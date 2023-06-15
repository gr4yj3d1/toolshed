from django.contrib import auth
from django.db import IntegrityError
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from authentication.models import ToolshedUser
from authentication.signature_auth import SignatureAuthenticationLocal
from hostadmin.models import Domain

router = routers.SimpleRouter()


class UserAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        try:
            fullname = request.data.get('username')
            username = fullname.split('@')[0]
            domain = fullname.split('@')[1]
            password = request.data.get('password')
            user = auth.authenticate(username=username, password=password, domain=domain)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'key': user.private_key
            })
        except IndexError:
            return Response({
                'error': 'Invalid Credentials'
            }, status=400)
        except IntegrityError:
            return Response({
                'error': 'Invalid Credentials'
            }, status=400)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ToolshedUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']


class UserViewSet(viewsets.ModelViewSet):
    queryset = ToolshedUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SignatureAuthenticationLocal])
def getUserInfo(request):
    user = request.user
    return Response({
        'username': user.username,
        'domain': user.domain,
        'email': user.email
    })


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def registerUser(request):
    try:
        username = request.data.get('username')
        domain = request.data.get('domain')
        password = request.data.get('password')
        email = request.data.get('email')

        errors = {}
        if not username:
            errors['username'] = 'Username is required'
        if not domain:
            errors['domain'] = 'Domain is required'
        if not password:
            errors['password'] = 'Password is required'
        if not email:
            errors['email'] = 'Email is required'
        if ToolshedUser.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
        if ToolshedUser.objects.filter(username=username, domain=domain).exists():
            errors['username'] = 'Username already exists'
        if errors:
            return Response({'errors': errors}, status=400)

        Domain.objects.get(name=domain, open_registration=True)

        user = ToolshedUser.objects.create_user(username, email, '', domain=domain)
        user.set_password(password)
        user.save()
        return Response({'username': user.username, 'domain': user.domain})
    except Domain.DoesNotExist:
        return Response({'errors': {'domain': 'Domain does not exist or is not open for registration'}}, status=400)


router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', getUserInfo),
    path('register/', registerUser),
    path('token/', UserAuthToken.as_view()),
]
