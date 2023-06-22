from authentication.tests import UserTestCase, SignatureAuthClient

client = SignatureAuthClient()


class FriendTestCase(UserTestCase):
    def setUp(self):
        super().setUp()

    def test_friendship_iternal(self):
        self.assertEqual(self.local_user1.friends.count(), 0)
        self.assertEqual(self.local_user2.friends.count(), 0)
        self.assertEqual(self.ext_user1.friends.count(), 0)
        self.assertEqual(self.ext_user2.friends.count(), 0)
        self.local_user1.friends.add(self.local_user2.public_identity)
        self.assertEqual(self.local_user1.friends.count(), 1)
        self.assertEqual(self.local_user2.friends.count(), 1)
        self.assertEqual(self.ext_user1.friends.count(), 0)
        self.assertEqual(self.ext_user2.friends.count(), 0)
        self.assertEqual(self.local_user1.friends.first(), self.local_user2.public_identity)
        self.assertEqual(self.local_user2.friends.first(), self.local_user1.public_identity)

    def test_friendship_external(self):
        self.assertEqual(self.local_user1.friends.count(), 0)
        self.assertEqual(self.local_user2.friends.count(), 0)
        self.assertEqual(self.ext_user1.friends.count(), 0)
        self.assertEqual(self.ext_user2.friends.count(), 0)
        self.local_user1.friends.add(self.ext_user1.public_identity)
        self.assertEqual(self.local_user1.friends.count(), 1)
        self.assertEqual(self.local_user2.friends.count(), 0)
        self.assertEqual(self.ext_user1.friends.count(), 1)
        self.assertEqual(self.ext_user2.friends.count(), 0)
        self.assertEqual(self.local_user1.friends.first(), self.ext_user1.public_identity)
        self.assertEqual(self.ext_user1.friends.first(), self.local_user1.public_identity)

    def test_friend_from_external(self):
        self.assertEqual(self.local_user1.friends.count(), 0)
        self.assertEqual(self.local_user2.friends.count(), 0)
        self.assertEqual(self.ext_user1.friends.count(), 0)
        self.assertEqual(self.ext_user2.friends.count(), 0)
        self.ext_user1.friends.add(self.local_user1.public_identity)
        self.assertEqual(self.local_user1.friends.count(), 1)
        self.assertEqual(self.local_user2.friends.count(), 0)
        self.assertEqual(self.ext_user1.friends.count(), 1)
        self.assertEqual(self.ext_user2.friends.count(), 0)
        self.assertEqual(self.local_user1.friends.first(), self.ext_user1.public_identity)
        self.assertEqual(self.ext_user1.friends.first(), self.local_user1.public_identity)


class FriendApiTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.local_user1.friends.add(self.local_user2.public_identity)
        self.local_user1.friends.add(self.ext_user1.public_identity)
        self.ext_user1.friends.add(self.local_user1.public_identity)

    def test_friend_list_internal1(self):
        reply = client.get('/api/friends/', self.local_user1)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 2)
        self.assertEqual(reply.json()[0]['username'], str(self.local_user2))
        self.assertEqual(reply.json()[1]['username'], str(self.ext_user1))

    def test_friend_list_internal2(self):
        reply = client.get('/api/friends/', self.local_user2)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 1)
        self.assertEqual(reply.json()[0]['username'], str(self.local_user1))

    def test_friend_list_external(self):
        reply = client.get('/api/friends/', self.ext_user1)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(len(reply.json()), 1)
        self.assertEqual(reply.json()[0]['username'], str(self.local_user1))
