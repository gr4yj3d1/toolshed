from django.test import TestCase, Client
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey

from authentication.models import ToolshedUser, KnownIdentity
from authentication.tests import UserTestCase, SignatureAuthClient
from hostadmin.models import Domain


class KnownIdentityTestCase(TestCase):
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


class UserModelTestCase(UserTestCase):
    def setUp(self):
        super().setUp()

    def test_admin(self):
        user = ToolshedUser.objects.get(username='admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(user.domain, 'localhost')
        self.assertEqual(user.email, 'admin@localhost')
        self.assertEqual(user.username, 'admin')

    def test_user(self):
        user = ToolshedUser.objects.get(username='testuser')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(user.domain, 'example.com')
        self.assertEqual(user.email, 'test@abc.de')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(len(user.private_key), 64)
        self.assertEqual(type(user.public_identity), KnownIdentity)
        self.assertEqual(user.public_identity.domain, 'example.com')
        self.assertEqual(user.public_identity.username, 'testuser')
        self.assertEqual(len(user.public_identity.public_key), 64)

    def test_create_existing_user(self):
        with self.assertRaises(ValueError):
            ToolshedUser.objects.create_user('testuser', 'test3@abc.de', '', domain='example.com')

    def test_create_existing_user2(self):
        key = SigningKey.generate()
        KnownIdentity.objects.create(username="testuser3", domain='localhost',
                                     public_key=key.verify_key.encode(encoder=HexEncoder).decode('utf-8'))
        with self.assertRaises(ValueError):
            ToolshedUser.objects.create_user('testuser3', 'test3@abc.de', '', domain='localhost')

    def test_create_reuse_email(self):
        with self.assertRaises(ValueError):
            ToolshedUser.objects.create_user('testuser3', 'test@abc.de', '', domain='example.com')

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
        user = self.local_user1
        message = 'some message'
        signature = user.sign(message)
        self.assertEqual(len(signature), 128)
        self.assertTrue(user.public_identity.verify(message, signature))

    def test_signature_fail(self):
        user = self.local_user1
        message = 'some message'
        signature = user.sign(message)
        self.assertFalse(user.public_identity.verify(message + 'x', signature))

    def test_signature_fail2(self):
        user = self.local_user1
        message = 'some message'
        signature = user.sign(message)
        signature = signature[:-2] + 'ee'
        self.assertFalse(user.public_identity.verify(message, signature))

    def test_signature_fail3(self):
        user1 = self.local_user1
        user2 = self.local_user2
        message = 'some message'
        signature = user1.sign(message)
        self.assertFalse(user2.public_identity.verify(message, signature))

    def test_signature_fail4(self):
        user = self.local_user1
        message = 'some message'
        with self.assertRaises(TypeError):
            user.sign(message.encode('utf-8'))


class UserApiTestCase(UserTestCase):

    def setUp(self):
        super().setUp()
        self.anonymous_client = Client(SERVER_NAME='testserver')
        self.client = SignatureAuthClient()

    def test_user_info(self):
        reply = self.client.get('/auth/user/', self.local_user1)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(reply.json()['username'], 'testuser')
        self.assertEqual(reply.json()['domain'], 'example.com')
        self.assertEqual(reply.json()['email'], 'test@abc.de')

    def test_user_info2(self):
        target = "/auth/user/"
        signature = self.local_user1.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.local_user1) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(reply.json()['username'], 'testuser')
        self.assertEqual(reply.json()['domain'], 'example.com')

    def test_user_info_fail(self):
        reply = self.anonymous_client.get('/auth/user/')
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail2(self):
        reply = self.client.get('/auth/user/', self.ext_user1)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail3(self):
        target = "/auth/user/"
        signature = self.local_user1.sign("http://testserver2" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.local_user1) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail4(self):
        target = "/auth/user/"
        signature = self.local_user1.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Auth ' + str(self.local_user1) + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail5(self):
        target = "/auth/user/"
        signature = self.local_user1.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.local_user1)}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail6(self):
        target = "/auth/user/"
        signature = self.local_user1.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(self.local_user1) + ':' + signature + 'f'}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail7(self):
        target = "/auth/user/"
        signature = self.local_user1.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + self.local_user1.username + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail8(self):
        target = "/auth/user/"
        signature = self.local_user1.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + self.local_user1.username + '@:' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)

    def test_user_info_fail9(self):
        target = "/auth/user/"
        signature = self.local_user1.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature @' + self.local_user1.domain + ':' + signature}
        reply = self.anonymous_client.get(target, **header)
        self.assertEqual(reply.status_code, 403)


class LoginApiTestCase(UserTestCase):
    user = None
    client = Client(SERVER_NAME='testserver')

    def setUp(self):
        super().setUp()
        self.user = self.local_user1

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


class RegistrationApiTestCase(TestCase):
    client = Client(SERVER_NAME='testserver')

    def setUp(self):
        admin = ToolshedUser.objects.create_superuser('admin', 'admin@localhost', '')
        admin.set_password('testpassword')
        admin.save()
        example_com = Domain.objects.create(name='example.com', owner=admin, open_registration=True)
        example_com.save()
        user2 = ToolshedUser.objects.create_user('testuser2', 'test2@abc.de', '', domain=example_com.name)
        user2.set_password('testpassword3')
        user2.save()

    def test_registration(self):
        self.assertEqual(ToolshedUser.objects.all().count(), 2)
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
        self.assertEqual(ToolshedUser.objects.all().count(), 3)

    def test_registration_fail(self):
        reply = self.client.post('/auth/register/',
                                 {'username': '', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('username' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_fail2(self):
        reply = self.client.post('/auth/register/',
                                 {'password': 'testpassword2', 'domain': 'example.com', 'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('username' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_fail3(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': '', 'domain': 'example.com',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('password' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_fail4(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'domain': 'example.com', 'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('password' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_fail5(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': '',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('domain' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_fail6(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('domain' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_fail7(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': ''})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('email' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_fail8(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.com'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('email' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_existing_user(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser2', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': 'test3@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        # TODO: check for sensible error message
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_foreign_domain(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.org',
                                  'email': 'test@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('domain' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)

    def test_registration_reuse_email(self):
        reply = self.client.post('/auth/register/',
                                 {'username': 'testuser', 'password': 'testpassword2', 'domain': 'example.com',
                                  'email': 'test2@abc.de'})
        self.assertEqual(reply.status_code, 400)
        self.assertTrue('errors' in reply.json())
        self.assertTrue('email' in reply.json()['errors'])
        self.assertEqual(ToolshedUser.objects.all().count(), 2)
