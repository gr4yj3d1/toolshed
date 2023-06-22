from django.test import Client
from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase
from authentication.models import FriendRequestIncoming, FriendRequestOutgoing

client = SignatureAuthClient()


class FriendTestCase(UserTestMixin, ToolshedTestCase):
    def setUp(self):
        super().setUp()
        self.prepare_users()

    def test_friendship_iternal(self):
        self.assertEqual(self.f['local_user1'].friends.count(), 0)
        self.assertEqual(self.f['local_user2'].friends.count(), 0)
        self.assertEqual(self.f['ext_user1'].friends.count(), 0)
        self.assertEqual(self.f['ext_user2'].friends.count(), 0)
        self.f['local_user1'].friends.add(self.f['local_user2'].public_identity)
        self.assertEqual(self.f['local_user1'].friends.count(), 1)
        self.assertEqual(self.f['local_user2'].friends.count(), 1)
        self.assertEqual(self.f['ext_user1'].friends.count(), 0)
        self.assertEqual(self.f['ext_user2'].friends.count(), 0)
        self.assertEqual(self.f['local_user1'].friends.first(), self.f['local_user2'].public_identity)
        self.assertEqual(self.f['local_user2'].friends.first(), self.f['local_user1'].public_identity)

    def test_friendship_external(self):
        self.assertEqual(self.f['local_user1'].friends.count(), 0)
        self.assertEqual(self.f['local_user2'].friends.count(), 0)
        self.assertEqual(self.f['ext_user1'].friends.count(), 0)
        self.assertEqual(self.f['ext_user2'].friends.count(), 0)
        self.f['local_user1'].friends.add(self.f['ext_user1'].public_identity)
        self.assertEqual(self.f['local_user1'].friends.count(), 1)
        self.assertEqual(self.f['local_user2'].friends.count(), 0)
        self.assertEqual(self.f['ext_user1'].friends.count(), 1)
        self.assertEqual(self.f['ext_user2'].friends.count(), 0)
        self.assertEqual(self.f['local_user1'].friends.first(), self.f['ext_user1'].public_identity)
        self.assertEqual(self.f['ext_user1'].friends.first(), self.f['local_user1'].public_identity)

    def test_friend_from_external(self):
        self.assertEqual(self.f['local_user1'].friends.count(), 0)
        self.assertEqual(self.f['local_user2'].friends.count(), 0)
        self.assertEqual(self.f['ext_user1'].friends.count(), 0)
        self.assertEqual(self.f['ext_user2'].friends.count(), 0)
        self.f['ext_user1'].friends.add(self.f['local_user1'].public_identity)
        self.assertEqual(self.f['local_user1'].friends.count(), 1)
        self.assertEqual(self.f['local_user2'].friends.count(), 0)
        self.assertEqual(self.f['ext_user1'].friends.count(), 1)
        self.assertEqual(self.f['ext_user2'].friends.count(), 0)
        self.assertEqual(self.f['local_user1'].friends.first(), self.f['ext_user1'].public_identity)
        self.assertEqual(self.f['ext_user1'].friends.first(), self.f['local_user1'].public_identity)


class FriendApiTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.f['local_user1'].friends.add(self.f['local_user2'].public_identity)
        self.f['local_user1'].friends.add(self.f['ext_user1'].public_identity)
        self.f['ext_user1'].friends.add(self.f['local_user1'].public_identity)

    def test_friend_list_internal1(self):
        reply = client.get('/api/friends/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 2)
        self.assertEqual(reply.json()[0]['username'], str(self.f['local_user2']))
        self.assertEqual(reply.json()[1]['username'], str(self.f['ext_user1']))

    def test_friend_list_internal2(self):
        reply = client.get('/api/friends/', self.f['local_user2'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 1)
        self.assertEqual(reply.json()[0]['username'], str(self.f['local_user1']))

    def test_friend_list_external(self):
        reply = client.get('/api/friends/', self.f['ext_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 1)
        self.assertEqual(reply.json()[0]['username'], str(self.f['local_user1']))


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


class FriendRequestListTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        FriendRequestIncoming.objects.create(
            befriender_username=self.f['ext_user2'].username, befriender_domain=self.f['ext_user2'].domain,
            befriender_public_key=self.f['ext_user2'].public_key(), befriendee_user=self.f['local_user1'],
            secret='secret1').save()

    def test_friend_request_withouth_auth(self):
        reply = Client().get('/api/friendrequests/')
        self.assertEqual(reply.status_code, 401)

    def test_friend_request_empty(self):
        reply = client.get('/api/friendrequests/', self.f['local_user2'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(reply.json(), [])

    def test_friend_request_list(self):
        reply = client.get('/api/friendrequests/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 1)
        self.assertEqual(reply.json()[0]['befriender'], str(self.f['ext_user2']))
        self.assertEqual(reply.json()[0]['befriender_public_key'], self.f['ext_user2'].public_key())


class FriendRequestIncomingTestCase(UserTestMixin, ToolshedTestCase):
    def setUp(self):
        super().setUp()
        self.prepare_users()
        FriendRequestIncoming.objects.create(
            befriender_username=self.f['ext_user2'].username, befriender_domain=self.f['ext_user2'].domain,
            befriender_public_key=self.f['ext_user2'].public_key(), befriendee_user=self.f['local_user1'],
            secret='secret1').save()

    def test_post_request(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriender_key': befriender.public_key(),
            'befriendee': str(befriendee),
            'secret': 'secret2'
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(reply.json()['status'], 'pending')
        self.assertEqual(FriendRequestIncoming.objects.count(), 2)
        incoming = FriendRequestIncoming.objects.get(befriender_username=befriender.username,
                                                     befriender_domain=befriender.domain)
        self.assertEqual(incoming.befriendee_user, befriendee)
        self.assertEqual(incoming.befriender_public_key, befriender.public_key())
        self.assertEqual(incoming.secret, 'secret2')

    def test_post_request_local(self):
        befriender = self.f['local_user2']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriendee': str(befriendee),
            # 'secret': 'secret2'
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(reply.json()['status'], 'pending')
        self.assertEqual(FriendRequestIncoming.objects.count(), 2)
        incoming = FriendRequestIncoming.objects.get(befriender_username=befriender.username,
                                                     befriender_domain=befriender.domain)
        self.assertEqual(incoming.befriendee_user, befriendee)
        self.assertEqual(incoming.befriender_public_key, befriender.public_key())
        # self.assertEqual(incoming.secret, 'secret2')

    def test_post_request_withouth_auth(self):
        reply = Client().post('/api/friendrequests/')
        self.assertEqual(reply.status_code, 400)

    def test_post_request_broken_header(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user1']
        broken_client = SignatureAuthClient(header_prefix='broken ')
        reply = broken_client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriender_key': befriender.public_key(),
            'befriendee': str(befriendee),
            'secret': 'secret2'
        })
        self.assertEqual(reply.status_code, 400)

    def test_post_request_missing_key(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriendee': str(befriendee),
            'secret': 'secret2'
        })
        self.assertEqual(reply.status_code, 400)

    def test_post_request_breaking_key(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriendee': str(befriendee),
            'secret': 'secret2',
            'befriender_key': 'broken'
        })
        self.assertEqual(reply.status_code, 400)

    def test_post_request_wrong_befriender(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(self.f['local_user2']),
            'befriender_key': befriender.public_key(),
            'befriendee': str(befriendee),
            'secret': 'secret2'
        })
        self.assertEqual(reply.status_code, 400)

    def test_post_request_bad_signature(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user1']
        bad_signature = SignatureAuthClient(bad_signature=True)
        reply = bad_signature.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriender_key': befriender.public_key(),
            'befriendee': str(befriendee),
            'secret': 'secret2'
        })
        self.assertEqual(reply.status_code, 400)

    def test_post_request_self(self):
        befriender = self.f['local_user1']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriender_key': befriender.public_key(),
            'befriendee': str(befriendee),
            'secret': 'secret2'
        })
        self.assertEqual(reply.status_code, 400)

    def test_post_request_befreindee_not_found(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriender_key': befriender.public_key(),
            'befriendee': 'nonexistent@' + befriendee.domain,
            'secret': 'secret2'
        })
        self.assertEqual(reply.status_code, 400)

    def test_post_request_missing_secret(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriender_key': befriender.public_key(),
            'befriendee': str(befriendee)
        })
        self.assertEqual(reply.status_code, 400)

    def test_accept_request(self):
        befriender = self.f['ext_user2']
        befriendee = self.f['local_user1']
        request = FriendRequestIncoming.objects.filter(befriender_username=befriender.username,
                                                       befriender_domain=befriender.domain,
                                                       befriendee_user=befriendee).first()
        reply = client.post('/api/friends/', befriendee, {
            'friend_request_id': request.id,
            'secret': request.secret
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(reply.json(), {'status': 'accepted'})

    def test_accept_request(self):
        befriender = self.f['ext_user2']
        befriendee = self.f['local_user1']
        request = FriendRequestIncoming.objects.filter(befriender_username=befriender.username,
                                                       befriender_domain=befriender.domain,
                                                       befriendee_user=befriendee).first()
        reply = client.post('/api/friends/', befriendee, {
            'friend_request_id': request.id,
            'secret': request.secret
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(reply.json(), {'status': 'accepted'})

    def test_accept_request_not_found(self):
        befriender = self.f['ext_user2']
        befriendee = self.f['local_user1']
        reply = client.post('/api/friends/', befriendee, {
            'friend_request_id': 999,
            'secret': 'secret1'
        })
        self.assertEqual(reply.status_code, 404)


class FriendRequestOutgoingTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        FriendRequestOutgoing.objects.create(
            befriender_user=self.f['local_user2'],
            befriendee_username=self.f['ext_user1'].username,
            befriendee_domain=self.f['ext_user1'].domain,
            secret='secret3'
        ).save()

    def test_post_outgoing_friend_request(self):
        befriender = self.f['local_user1']
        befriendee = self.f['ext_user1']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriendee': str(befriendee),
        })
        self.assertEqual(reply.status_code, 201)
        self.assertTrue('status' in reply.json())
        self.assertEqual(reply.json()['status'], 'pending')
        self.assertEqual(FriendRequestOutgoing.objects.count(), 2)
        outgoing = FriendRequestOutgoing.objects.get(befriender_user=befriender)
        self.assertTrue('secret' in reply.json())
        self.assertEqual(reply.json()['secret'], outgoing.secret)
        self.assertEqual(outgoing.befriendee_username, befriendee.username)
        self.assertEqual(outgoing.befriendee_domain, befriendee.domain)

    def test_accept_request(self):
        befriender = self.f['ext_user1']
        befriendee = self.f['local_user2']
        reply = client.post('/api/friendrequests/', befriender, {
            'befriender': str(befriender),
            'befriender_key': befriender.public_key(),
            'befriendee': str(befriendee),
            'secret': 'secret3'
        })
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(reply.json(), {'status': 'accepted'})
        self.assertEqual(FriendRequestIncoming.objects.count(), 0)
        self.assertEqual(FriendRequestOutgoing.objects.count(), 0)
        self.assertEqual(befriendee.friends.count(), 1)
        self.assertEqual(befriendee.friends.first().username, befriender.username)
        self.assertEqual(befriendee.friends.first().domain, befriender.domain)
