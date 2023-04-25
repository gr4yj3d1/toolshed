from django.urls import path
from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from authentication.models import KnownIdentity, FriendRequestIncoming, FriendRequestOutgoing
from toolshed.auth import SignatureAuthentication


# TODO this entire file doesn't do anything, even though it might look like it does.

# what ~should~ happen:
# 1. user x@A sends a friend request to user y@B
#   1.1. x@A's client sends a POST request to A/api/friendrequests/ with body {from: x@A, to: y@B}
#   1.2. A's backend creates a FriendRequestOutgoing object, containing x@A's identity and y@B's name
#   1.3. x@A's client sends a POST request to B/api/friendrequests/ with body
#                       {from: x@A, to: y@B, public_key: x@A's public key}
#   1.4. B's backend creates a FriendRequestIncoming object, containing y@B's and x@A's identities
# 2. user y@B accepts the friend request
#   2.1. y@B's client sends a POST request to A/api/friendsrequests/ with body
#                       {from: x@A, to: y@B, public_key: y@B's public key}
#   2.2. A's backend matches the data to the FriendRequestOutgoing object, deletes both and  creates a Friend object,
#       containing x@A's and y@B's identities
#   2.3. y@B's client sends a POST request to B/api/friends/ containing the id of the FriendRequestIncoming object
#   2.4. B's backend creates a Friend object, using the identities from the FriendRequestIncoming object


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnownIdentity
        fields = ['username', 'domain']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnownIdentity
        fields = ['from_identity', 'to_identity']


class Friends(APIView, ViewSetMixin):
    # authentication_classes = [SignatureAuthentication, TokenAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):  # /api/friends/
        user = request.user
        friends = user.friends.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # /api/friends/
        user = request.user
        friend = get_object_or_404(user.friends_requests.all(), pk=request.data['friend'])
        user.friends.add(friend)
        user.save()
        serializer = FriendSerializer(friend)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def declineFriendRequest(request, pk, format=None):  # /api/friends/<id>/
    user = request.user
    friend = get_object_or_404(user.friends, pk=pk)
    user.friends.remove(friend)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class FriendsRequests(APIView, ViewSetMixin):
    # authentication_classes = [SignatureAuthentication, TokenAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):  # /api/friendrequests/
        user = request.user
        if user.is_authenticated:
            friends_requests = user.friends_requests.all()
        else:
            friends_requests = FriendRequestIncoming.objects.all()
        serializer = FriendSerializer(friends_requests, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # /api/friendrequests/
        user = request.user
        if user.is_authenticated:
            friend = get_object_or_404(user.friends_requests.all(), pk=request.data['friend'])
            user.friends.add(friend)
            user.save()
        else:
            friend = get_object_or_404(FriendRequestIncoming.objects.all(), pk=request.data['friend'])
            friend.accepted = True
            friend.save()
        serializer = FriendSerializer(friend)
        return Response(serializer.data)


@api_view(['DELETE'])
def deleteFriendRequest(request, pk, format=None):  # /api/friendrequests/<id>/
    user = request.user
    friend = get_object_or_404(user.friends_requests.all(), pk=pk)
    user.friends_requests.remove(friend)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


urlpatterns = [
    path('friends/', Friends.as_view(), name='friends'),
    path('friends/<int:pk>/', declineFriendRequest),
    path('friendrequests/', FriendsRequests.as_view(), name='friendrequests'),
    path('friendrequests/<int:pk>/', deleteFriendRequest),
]
