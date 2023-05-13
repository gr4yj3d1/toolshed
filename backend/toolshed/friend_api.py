import secrets

from django.urls import path
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from authentication.models import KnownIdentity, FriendRequestIncoming, FriendRequestOutgoing
from toolshed.auth import verify_incoming_friend_request, split_userhandle_or_throw, \
    authenticate_request_against_local_users, SignatureAuthentication
from authentication.models import ToolshedUser


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
    befriender = serializers.SerializerMethodField()

    def get_befriender(self, obj):
        return obj.befriender_username + '@' + obj.befriender_domain

    class Meta:
        model = FriendRequestIncoming
        fields = ['befriender', 'befriender_public_key', 'secret']


class Friends(APIView, ViewSetMixin):
    authentication_classes = [SignatureAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):  # /api/friends/ # TODO what should this do?
        user = request.user
        friends = user.friends.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # /api/friends/
        # only for local users
        user = request.user
        incomingrequest = FriendRequestIncoming.objects.get(pk=request.data.get('friend_request_id'))
        befriender = KnownIdentity.objects.create(
            username=incomingrequest.befriender_username,
            domain=incomingrequest.befriender_domain,
            public_key=incomingrequest.befriender_public_key
        )
        ToolshedUser.objects.get(user=user).friends.add(befriender)
        return Response(status=status.HTTP_201_CREATED, data={'status': 'accepted'})


@api_view(['DELETE'])
def declineFriendRequest(request, pk, format=None):  # /api/friends/<id>/
    user = request.user
    friend = get_object_or_404(user.friends, pk=pk)
    user.friends.remove(friend)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class FriendsRequests(APIView, ViewSetMixin):
    def get(self, request, format=None):  # /api/friendrequests/  # TODO what should this do?
        user = request.user
        if user.is_authenticated:
            friends_requests = user.friends_requests.all()
        else:
            friends_requests = FriendRequestIncoming.objects.all()
        serializer = FriendRequestSerializer(friends_requests, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # /api/friendrequests/
        raw_request = request.body.decode('utf-8')
        befriender_username, befriender_domain = split_userhandle_or_throw(request.data['befriender'])
        befriendee_username, befriendee_domain = split_userhandle_or_throw(request.data['befriendee'])
        if user := authenticate_request_against_local_users(request, raw_request):
            secret = secrets.token_hex(64)
            FriendRequestOutgoing.objects.create(
                befriender_user=user,
                befriendee_username=befriendee_username,
                befriendee_domain=befriendee_domain,
                secret=secret,
            )
            return Response(status=status.HTTP_201_CREATED, data={'secret': secret, 'status': "pending"})
        elif verify_incoming_friend_request(request, raw_request):
            try:
                befriendee = ToolshedUser.objects.get(username=befriendee_username, domain=befriendee_domain)

                outgoing = FriendRequestOutgoing.objects.filter(
                    secret=request.data['secret'],
                    befriender_user=befriendee,  # both sides match
                    befriendee_username=befriender_username,
                    befriendee_domain=befriender_domain)
                if outgoing.exists():
                    befriender = KnownIdentity.objects.create(
                        username=befriender_username,
                        domain=befriender_domain,
                        public_key=request.data['befriender_key']
                    )
                    befriendee.friends.add(befriender)
                    return Response(status=status.HTTP_201_CREATED, data={'status': "accepted"})
                else:
                    FriendRequestIncoming.objects.create(
                        befriender_username=befriender_username,
                        befriender_domain=befriender_domain,
                        befriender_public_key=request.data['befriender_key'],
                        befriendee_user=befriendee,
                        secret=request.data['secret']
                    )
                    return Response(status=status.HTTP_201_CREATED, data={'status': "pending"})
            except ToolshedUser.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
