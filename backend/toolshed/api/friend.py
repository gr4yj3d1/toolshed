from django.urls import path
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from authentication.signature_auth import SignatureAuthentication
from toolshed.serializers import FriendSerializer


class Friends(APIView, ViewSetMixin):
    authentication_classes = [SignatureAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):  # /api/friends/ #
        user = request.user
        friends = user.friends.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)


urlpatterns = [
    path('friends/', Friends.as_view(), name='friends'),
]
