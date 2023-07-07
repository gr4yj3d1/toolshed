import json

from django.test import Client, RequestFactory
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey

from authentication.models import ToolshedUser, KnownIdentity
from authentication.tests import UserTestMixin, SignatureAuthClient, DummyExternalUser, ToolshedTestCase


class AuthorizationTestCase(ToolshedTestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        from nacl.signing import SigningKey
        self.key = SigningKey.generate()
        self.signature = self.key.sign("test".encode('utf-8'), encoder=HexEncoder).signature.decode('utf-8')
        self.data = json.dumps({'a': 'b'})
        self.signature_with_data = self.key.sign(
            ("test" + self.data).encode('utf-8'), encoder=HexEncoder).signature.decode('utf-8')

    def test_parse_auth_header(self):
        request = self.factory.get('/test')
        from authentication.signature_auth import verify_request
        with self.assertRaises(ValueError):
            verify_request(request, "")

    def test_parse_auth_header2(self):
        request = self.factory.get('/test', HTTP_AUTHORIZATION="Signature ")
        from authentication.signature_auth import verify_request
        with self.assertRaises(ValueError):
            verify_request(request, "")

    def test_parse_auth_header3(self):
        request = self.factory.get('/test', HTTP_AUTHORIZATION="Signature author@domain")
        from authentication.signature_auth import verify_request
        with self.assertRaises(ValueError):
            verify_request(request, "")

    def test_parse_auth_header4(self):
        from authentication.signature_auth import verify_request
        request = self.factory.get('/test', HTTP_AUTHORIZATION="Signature author@domain:" + self.signature)
        username, domain, signed_data, signature_bytes_hex = verify_request(request, "")
        self.assertEqual(username, "author")
        self.assertEqual(domain, "domain")
        self.assertEqual(signed_data, "http://testserver/test")
        self.assertEqual(signature_bytes_hex, self.signature)

    def test_parse_auth_header5(self):
        from authentication.signature_auth import verify_request
        request = self.factory.post('/test', self.data, content_type="application/json",
                                    HTTP_AUTHORIZATION="Signature author@domain:" + self.signature_with_data)
        username, domain, signed_data, signature_bytes_hex = verify_request(request, request.body.decode('utf-8'))
        self.assertEqual(username, "author")
        self.assertEqual(domain, "domain")
        self.assertEqual(signed_data, "http://testserver/test" + self.data)
        self.assertEqual(signature_bytes_hex, self.signature_with_data)

    def test_parse_auth_header6(self):
        from authentication.signature_auth import verify_request
        request = self.factory.put('/test', self.data, content_type="application/json",
                                   HTTP_AUTHORIZATION="Signature author@domain:" + self.signature_with_data)
        username, domain, signed_data, signature_bytes_hex = verify_request(request, request.body.decode('utf-8'))
        self.assertEqual(username, "author")
        self.assertEqual(domain, "domain")
        self.assertEqual(signed_data, "http://testserver/test" + self.data)
        self.assertEqual(signature_bytes_hex, self.signature_with_data)

    def test_parse_auth_header7(self):
        from authentication.signature_auth import verify_request
        request = self.factory.delete('/test', HTTP_AUTHORIZATION="Signature author@domain:" + self.signature)
        username, domain, signed_data, signature_bytes_hex = verify_request(request, request.body.decode('utf-8'))
        self.assertEqual(username, "author")
        self.assertEqual(domain, "domain")
        self.assertEqual(signed_data, "http://testserver/test")
        self.assertEqual(signature_bytes_hex, self.signature)

    def test_parse_auth_header8(self):
        from authentication.signature_auth import verify_request
        request = self.factory.patch('/test', self.data, content_type="application/json",
                                     HTTP_AUTHORIZATION="Signature author@domain:" + self.signature_with_data)
        username, domain, signed_data, signature_bytes_hex = verify_request(request, request.body.decode('utf-8'))
        self.assertEqual(username, "author")
        self.assertEqual(domain, "domain")
        self.assertEqual(signed_data, "http://testserver/test" + self.data)
        self.assertEqual(signature_bytes_hex, self.signature_with_data)


class KnownIdentityTestCase(ToolshedTestCase):
    key = None

    def setUp(self):
        self.key = SigningKey.generate()
        KnownIdentity.objects.create(username="testuser", domain='external.com',
                                     public_key=self.key.verify_key.encode(encoder=HexEncoder).decode('utf-8'))

    def test_known_identity(self):
        identity = KnownIdentity.objects.get(username="testuser", domain='external.com')
        self.assertEqual(identity.username, "testuser")
        self.assertEqual(identity.domain, "external.com")
        self.assertEqual(identity.public_key, self.key.verify_key.encode(encoder=HexEncoder).decode('utf-8'))
        self.assertEqual(str(identity), "testuser@external.com")
        self.assertTrue(identity.is_authenticated())

    def test_known_identity_verify(self):
        identity = KnownIdentity.objects.get(username="testuser", domain='external.com')
        message = "Hello world, this is a test message."
        signed = self.key.sign(message.encode('utf-8'), encoder=HexEncoder).signature
        self.assertTrue(identity.verify(message, signed.decode('utf-8')))

    def test_known_identity_verify_fail(self):
        identity = KnownIdentity.objects.get(username="testuser", domain='external.com')
        message = "Hello world, this is a test message."
        signed = self.key.sign(message.encode('utf-8'), encoder=HexEncoder).signature
        self.assertFalse(identity.verify(message + "x", signed.decode('utf-8')))

    def test_known_identity_verify_fail2(self):
        identity = KnownIdentity.objects.get(username="testuser", domain='external.com')
        message = "Hello world, this is a test message."
        signed = self.key.sign(message.encode('utf-8'), encoder=HexEncoder).signature
        with self.assertRaises(TypeError):
            identity.verify(message.encode('utf-8'), signed.decode('utf-8'))

    def test_known_identity_verify_fail3(self):
        identity = KnownIdentity.objects.get(username="testuser", domain='external.com')
        message = "Hello world, this is a test message."
        signed = self.key.sign(message.encode('utf-8'), encoder=HexEncoder).signature
        with self.assertRaises(TypeError):
            identity.verify(message, signed)

    def test_known_identity_verify_fail4(self):
        identity = KnownIdentity.objects.get(username="testuser", domain='external.com')
        message = "Hello world, this is a test message."
        signed = self.key.sign(message.encode('utf-8'), encoder=HexEncoder).signature
        with self.assertRaises(TypeError):
            identity.verify(message, bytes.fromhex(signed.decode('utf-8')))


class UserModelTestCase(UserTestMixin, ToolshedTestCase):
    def setUp(self):
        super().setUp()
        self.prepare_users()

    def test_admin(self):
        user = self.f['admin']
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(user.domain, 'localhost')
        self.assertEqual(user.email, 'testadmin@localhost')
        self.assertEqual(user.username, 'testadmin')

    def test_user(self):
        user = self.f['local_user1']
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(user.domain, 'example.com')
        self.assertEqual(user.email, 'test1@abc.de')
        self.assertEqual(user.username, 'testuser1')
        self.assertEqual(len(user.private_key), 64)
        self.assertEqual(type(user.public_identity), KnownIdentity)
        self.assertEqual(user.public_identity.domain, 'example.com')
        self.assertEqual(user.public_identity.username, 'testuser1')
        self.assertEqual(len(user.public_identity.public_key), 64)

    def test_create_existing_user(self):
        with self.assertRaises(ValueError):
            ToolshedUser.objects.create_user('testuser1', 'test3@abc.de', 'testpassword', domain='example.com')

    def test_create_existing_user2(self):
        key = SigningKey.generate()
        KnownIdentity.objects.create(username="testuser3", domain='localhost',
                                     public_key=key.verify_key.encode(encoder=HexEncoder).decode('utf-8'))
        with self.assertRaises(ValueError):
            ToolshedUser.objects.create_user('testuser3', 'test3@abc.de', 'testpassword', domain='localhost')

    def test_create_reuse_email(self):
        with self.assertRaises(ValueError):
            ToolshedUser.objects.create_user('testuser3', 'test1@abc.de', 'testpassword', domain='example.com')

    def test_create_user_invalid_private_key(self):
        with self.assertRaises(TypeError):
            ToolshedUser.objects.create_user('testuser3', 'test3@abc.de', '', domain='example.com',
                                             private_key=b'0123456789abcdef0123456789abcdef')
        with self.assertRaises(ValueError):
            ToolshedUser.objects.create_user('testuser3', 'test3@abc.de', '', domain='example.com',
                                             private_key='7005c4097')
        with self.assertRaises(ValueError):
            ToolshedUser.objects.create_user('testuser3', 'test3@abc.de', '', domain='example.com',
                                             private_key='0123456789abcdef0123456789abcdef'
                                                         'Z123456789abcdef0123456789abcdef')

    def test_signature(self):
        user = self.f['local_user1']
        message = 'some message'
        signature = user.sign(message)
        self.assertEqual(len(signature), 128)
        self.assertTrue(user.public_identity.verify(message, signature))

    def test_signature_fail(self):
        user = self.f['local_user1']
        message = 'some message'
        signature = user.sign(message)
        self.assertFalse(user.public_identity.verify(message + 'x', signature))

    def test_signature_fail2(self):
        user = self.f['local_user1']
        message = 'some message'
        signature = user.sign(message)
        signature = signature[:-2] + 'ee'
        self.assertFalse(user.public_identity.verify(message, signature))

    def test_signature_fail3(self):
        user1 = self.f['local_user1']
        user2 = self.f['local_user2']
        message = 'some message'
        signature = user1.sign(message)
        self.assertFalse(user2.public_identity.verify(message, signature))

    def test_signature_fail4(self):
        user = self.f['local_user1']
        message = 'some message'
        with self.assertRaises(TypeError):
            user.sign(message.encode('utf-8'))


class UserApiTestCase(UserTestMixin, ToolshedTestCase):

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.anonymous_client = Client(SERVER_NAME='testserver')
        self.client = SignatureAuthClient()

    def test_user_info(self):
        reply = self.client.get('/auth/user/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(reply.json()['username'], 'testuser1')
        self.assertEqual(reply.json()['domain'], 'example.com')
        self.assertEqual(reply.json()['email'], 'test1@abc.de')

    def test_user_info2(self):
        target = "/auth/user/"
        signature = self.f['local_user1'].sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.f['local_user1']) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(reply.json()['username'], 'testuser1')
        self.assertEqual(reply.json()['domain'], 'example.com')

    def test_user_info_fail(self):
        reply = self.anonymous_client.get('/auth/user/')
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail2(self):
        reply = self.client.get('/auth/user/', self.f['ext_user1'])
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail3(self):
        target = "/auth/user/"
        signature = self.f['local_user1'].sign("http://testserver2" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.f['local_user1']) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail4(self):
        target = "/auth/user/"
        signature = self.f['local_user1'].sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Auth ' + str(self.f['local_user1']) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail5(self):
        target = "/auth/user/"
        signature = self.f['local_user1'].sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.f['local_user1'])}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail6(self):
        target = "/auth/user/"
        signature = self.f['local_user1'].sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.f['local_user1']) + ':' + signature + 'f'}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail7(self):
        target = "/auth/user/"
        signature = self.f['local_user1'].sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + self.f['local_user1'].username + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail8(self):
        target = "/auth/user/"
        signature = self.f['local_user1'].sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + self.f['local_user1'].username + '@:' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail9(self):
        target = "/auth/user/"
        signature = self.f['local_user1'].sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature @' + self.f['local_user1'].domain + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)


class FriendApiTestCase(UserTestMixin, ToolshedTestCase):
    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.f['local_user1'].friends.add(self.f['local_user2'].public_identity)
        self.f['local_user1'].friends.add(self.f['ext_user1'].public_identity)
        self.f['ext_user1'].friends.add(self.f['local_user1'].public_identity)
        self.anonymous_client = Client(SERVER_NAME='testserver')
        self.client = SignatureAuthClient()

    def test_friend_local(self):
        reply = self.client.get('/api/friends/', self.f['local_user1'])
        self.assertEqual(reply.status_code, 200)

    def test_friend_external(self):
        reply = self.client.get('/api/friends/', self.f['ext_user1'])
        self.assertEqual(reply.status_code, 200)

    def test_friend_fail(self):
        reply = self.anonymous_client.get('/api/friends/')
        self.assertEqual(reply.status_code, 403)

    def test_friend_fail2(self):
        target = "/api/friends/"
        signature = self.f['local_user1'].sign("http://testserver2" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.f['local_user1']) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_friend_fail3(self):
        target = "/api/friends/"
        unknown_user = DummyExternalUser('extuser3', 'external.org', False)
        signature = unknown_user.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(unknown_user) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_friend_fail4(self):
        target = "/api/friends/"
        signature = self.f['local_user1'].sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Auth ' + str(self.f['local_user1']) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)


class LoginApiTestCase(UserTestMixin, ToolshedTestCase):
    user = None
    client = Client(SERVER_NAME='testserver')

    def setUp(self):
        super().setUp()
        self.prepare_users()
        self.user = self.f['local_user1']

    def test_login(self):
        reply = self.client.post('/auth/token/',
                                 {'username': self.user.username + '@' + self.user.domain, 'password': 'testpassword2'})
        self.assertEqual(reply.status_code, 200)
        self.assertTrue('token' in reply.json())
        self.assertTrue(len(reply.json()['token']) == 40)
        self.assertTrue('key' in reply.json())
        self.assertEqual(len(reply.json()['key']), 64)

    def test_login_fail(self):
        reply = self.client.post('/auth/token/',
                                 {'username': self.user.username + '@' + self.user.domain, 'password': 'testpassword3'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('token' not in reply.json())
        self.assertTrue('error' in reply.json())

    def test_login_fail2(self):
        reply = self.client.post('/auth/token/',
                                 {'username': self.user.username, 'password': 'testpassword2'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('token' not in reply.json())
        self.assertTrue('error' in reply.json())


class RegistrationApiTestCase(UserTestMixin, ToolshedTestCase):
    client = Client(SERVER_NAME='testserver')

    def setUp(self):
        super().setUp()
        self.prepare_users()

    def test_registration(self):
        self.assertEqual(ToolshedUser.objects.all().count(), 3)
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 200)
        self.assertTrue('username' in reply.json())
        self.assertTrue('domain' in reply.json())
        user = ToolshedUser.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@abc.de')
        self.assertEqual(user.domain, 'example.com')
        self.assertTrue(user.check_password('testpassword2'))
        self.assertEqual(ToolshedUser.objects.all().count(), 4)

    def test_registration_fail(self):
        reply = self.client.post('/auth/register/',
                                 {'username': '', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('username' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_fail2(self):
        reply = self.client.post('/auth/register/',
                                 {'password': 'testpassword2', 'domain': 'example.com', 'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('username' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_fail3(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': '', 'domain': 'example.com',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('password' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_fail4(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'domain': 'example.com', 'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('password' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_fail5(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': '',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('domain' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_fail6(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('domain' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_fail7(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': ''})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('email' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_fail8(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.com'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('email' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_existing_user(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser2', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': 'test3@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        # TODO: check for sensible error message
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_foreign_domain(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.org',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('domain' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_reuse_email(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': 'test2@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('email' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 3)
