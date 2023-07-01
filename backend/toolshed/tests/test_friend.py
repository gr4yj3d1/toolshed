from authentication.tests import SignatureAuthClient, UserTestMixin, ToolshedTestCase

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
