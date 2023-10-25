import secrets

from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from authentication.models import KnownIdentity, FriendRequestIncoming, FriendRequestOutgoing, ToolshedUser
from authentication.signature_auth import verify_incoming_friend_request, split_userhandle_or_throw, \
    authenticate_request_against_local_users, SignatureAuthenticationLocal, SignatureAuthentication
from toolshed.serializers import FriendSerializer, FriendRequestSerializer


class Friends(APIView, ViewSetMixin):
    authentication_classes = [SignatureAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):  # /api/friends/ #
        user = request.user
        friends = user.friends.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # /api/friends/
        # only for local users
        try:
            user = request.user
            incoming_request = FriendRequestIncoming.objects.get(
                pk=request.data.get('friend_request_id'),
                secret=request.data.get('secret'))
            befriender, _ = KnownIdentity.objects.get_or_create(
                username=incoming_request.befriender_username,
                domain=incoming_request.befriender_domain,
                public_key=incoming_request.befriender_public_key
            )
            befriender.save()
            user.user.get().friends.add(befriender)
            user.user.get().save()
            incoming_request.delete()
            return Response(status=status.HTTP_201_CREATED, data={'status': 'accepted'})
        except FriendRequestIncoming.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'status': 'not found'})


class FriendsRequests(APIView, ViewSetMixin):
    def get(self, request, format=None):  # /api/friendrequests/
        raw_request = request.body.decode('utf-8')
        if user := authenticate_request_against_local_users(request, raw_request):
            friends_requests = user.friend_requests_incoming.all()
            serializer = FriendRequestSerializer(friends_requests, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'status': 'unauthorized'})

    def post(self, request, format=None):  # /api/friendrequests/
        raw_request = request.body.decode('utf-8')
        if 'befriender' not in request.data or 'befriendee' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'status': 'missing parameters'})
        befriender_username, befriender_domain = split_userhandle_or_throw(request.data['befriender'])
        befriendee_username, befriendee_domain = split_userhandle_or_throw(request.data['befriendee'])
        if befriender_domain == befriendee_domain and befriender_username == befriendee_username:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'status': 'cannot befriend yourself'})
        if user := authenticate_request_against_local_users(request, raw_request):
            secret = secrets.token_hex(64)
            befriendee_user = ToolshedUser.objects.filter(username=befriendee_username, domain=befriendee_domain)
            if befriendee_user.exists():
                FriendRequestIncoming.objects.create(
                    befriender_username=befriender_username,
                    befriender_domain=befriender_domain,
                    befriender_public_key=user.public_identity.public_key,
                    secret=secret,  # request.data['secret'] # TODO ??
                    befriendee_user=befriendee_user.get(),
                )
                return Response(status=status.HTTP_201_CREATED, data={'secret': secret, 'status': "pending"})
            else:
                FriendRequestOutgoing.objects.create(
                    befriender_user=user,
                    befriendee_username=befriendee_username,
                    befriendee_domain=befriendee_domain,
                    secret=secret,  # request.data['secret'] # TODO ??
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
                    befriender, _ = KnownIdentity.objects.get_or_create(
                        username=befriender_username,
                        domain=befriender_domain,
                        public_key=request.data['befriender_key']
                    )
                    befriender.save()
                    befriendee.friends.add(befriender)
                    befriendee.save()
                    outgoing.delete()
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
@authentication_classes([SignatureAuthenticationLocal])
@permission_classes([IsAuthenticated])
def dropFriend(request, pk, format=None):  # /api/friends/<id>/
    user = request.user
    friend = get_object_or_404(user.friends, pk=pk)
    user.friends.remove(friend)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@authentication_classes([SignatureAuthenticationLocal])
@permission_classes([IsAuthenticated])
def deleteFriendRequest(request, pk, format=None):  # /api/friendrequests/<id>/
    user = request.user
    get_object_or_404(user.friend_requests_incoming, pk=pk).delete()
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


urlpatterns = [
    path('friends/', Friends.as_view(), name='friends'),
    path('friends/<int:pk>/', dropFriend),
    path('friendrequests/', FriendsRequests.as_view(), name='friendrequests'),
    path('friendrequests/<int:pk>/', deleteFriendRequest),
]
