import json

from django.test import TestCase, Client
from nacl.encoding import HexEncoder

from authentication.models import ToolshedUser, KnownIdentity
from nacl.signing import SigningKey


class DummyExternalUser:
    def __init__(self, username, domain, known=True):
        self.username = username
        self.domain = domain
        self.__signing_key = SigningKey.generate()
        self.public_identity, _ = KnownIdentity.objects.get_or_create(
            username=username,
            domain=domain,
            public_key=self.public_key()) if known else None

    def __str__(self):
        return self.username + '@' + self.domain

    def sign(self, message):
        return self.__signing_key.sign(message.encode('utf-8'), encoder=HexEncoder).signature.decode('utf-8')

    def public_key(self):
        return self.__signing_key.verify_key.encode(encoder=HexEncoder).decode('utf-8')

    @property
    def friends(self):
        return self.public_identity.friends


class SignatureAuthClient:
    base = Client(SERVER_NAME='testserver')

    def get(self, target, user, **kwargs):
        signature = user.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.get(target, **header, **kwargs)

    def post(self, target, user, data, **kwargs):
        json_data = json.dumps(data, separators=(',', ':'))
        signature = user.sign("http://testserver" + target + json_data)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.post(target, json_data, **header, content_type='application/json', **kwargs)

    def put(self, target, user, data, **kwargs):
        json_data = json.dumps(data, separators=(',', ':'))
        signature = user.sign("http://testserver" + target + json_data)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.put(target, json_data, **header, content_type='application/json', **kwargs)

    def patch(self, target, user, data, **kwargs):
        json_data = json.dumps(data, separators=(',', ':'))
        signature = user.sign("http://testserver" + target + json_data)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.patch(target, json_data, **header, content_type='application/json', **kwargs)

    def delete(self, target, user, **kwargs):
        signature = user.sign("http://testserver" + target)
        header = {'HTTP_AUTHORIZATION': 'Signature ' + str(user) + ':' + signature}
        return self.base.delete(target, **header, **kwargs)


class UserTestCase(TestCase):
    ext_user1 = None
    ext_user2 = None
    local_user1 = None
    local_user2 = None

    def setUp(self):
        admin = ToolshedUser.objects.create_superuser('admin', 'admin@localhost', '')
        admin.set_password('testpassword')
        admin.save()
        example_com = type('obj', (object,), {'name': 'example.com'})
        self.local_user1 = ToolshedUser.objects.create_user('testuser', 'test@abc.de', '', domain=example_com.name)
        self.local_user1.set_password('testpassword2')
        self.local_user1.save()
        self.local_user2 = ToolshedUser.objects.create_user('testuser2', 'test2@abc.de', '', domain=example_com.name)
        self.local_user2.set_password('testpassword3')
        self.local_user2.save()
        self.ext_user1 = DummyExternalUser('extuser1', 'external.org')
        self.ext_user2 = DummyExternalUser('extuser2', 'external.org')
